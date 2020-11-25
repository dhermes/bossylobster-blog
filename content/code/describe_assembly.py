import argparse
import collections
import os
import subprocess
import sys
import tempfile


IS_MACOS = sys.platform == "darwin"
IS_LINUX = sys.platform in ("linux", "linux2")
F90_TEMPLATE = """\
module pow{n}_mod
  use, intrinsic :: iso_c_binding, only: c_double
  implicit none
  public pow{n}
contains
  subroutine pow{n}(a, b) bind(c, name='pow{n}')
    real(c_double), intent(in) :: a
    real(c_double), intent(out) :: b
    b = a**{n}
  end subroutine pow{n}
end module pow{n}_mod
"""
VAR_NAME = "a"
DISASSEMBLED_PREAMBLE_LINUX = """\

{obj_path}:     file format elf64-x86-64


Disassembly of section .text:

0000000000000000 <pow{n}>:
"""
DISASSEMBLED_PREAMBLE_MACOS = """\

{obj_path}:\tfile format Mach-O 64-bit x86-64


Disassembly of section __TEXT,__text:

0000000000000000 _pow{n}:
"""
Instruction = collections.namedtuple(
    "Instruction", ["raw", "name", "arguments"]
)
MOVE_TO_OUTPUT = Instruction(
    raw=b"\xf2\x0f\x11\x06", name="movsd", arguments=("%xmm0", "(%rsi)")
)
RETURN = Instruction(raw=b"\xc3", name="retq", arguments=None)
MOVAPD = "movapd"
MOVSD = "movsd"
MULSD = "mulsd"


def to_bytes(as_hex):
    return bytes(int(pair, 16) for pair in as_hex.split())


def pretty(instruction):
    # First, turn "raw" into something pretty.
    raw_hex = ["{:02x}".format(char) for char in instruction.raw]
    return "{:11}     {:6}  [{:>6}, {:<6}]".format(
        " ".join(raw_hex), instruction.name, *instruction.arguments
    )


def get_register(register):
    if not register.startswith("%xmm"):
        raise ValueError("Unexpected register string", register)

    return int(register[4:])


def get_input_register(instruction):
    if instruction.name != MOVSD:
        raise ValueError("Unexpected initial instruction", instruction)
    if instruction.arguments is None or len(instruction.arguments) != 2:
        raise ValueError("Unexpected initial instruction", instruction)
    if instruction.arguments[0] != "(%rdi)":
        raise ValueError("Unexpected initial instruction", instruction)

    return get_register(instruction.arguments[1])


def get_output_register(instruction):
    if instruction.name != MOVSD:
        raise ValueError("Unexpected instruction before return", instruction)
    if instruction.arguments is None or len(instruction.arguments) != 2:
        raise ValueError("Unexpected instruction before return", instruction)
    if instruction.arguments[1] != "(%rsi)":
        raise ValueError("Unexpected instruction before return", instruction)

    return get_register(instruction.arguments[0])


def verify_last_register(instruction):
    if instruction != RETURN:
        raise ValueError("Unexpected return instruction", instruction)


def parse_disassembled(disassembled, preamble):
    if not disassembled.startswith(preamble):
        raise ValueError("Unexpected disassembled output", disassembled)

    _, disassembled_pow = disassembled.split(preamble, 1)

    lines = disassembled_pow.rstrip().split("\n")
    offset = 0
    instructions = []
    for line in lines:
        hex_offset, remaining = line.lstrip().split(":", 1)
        if int(hex_offset, 16) != offset:
            raise ValueError("Unexpected disassembled output", disassembled)
        remaining = remaining.lstrip()
        raw_bytes = to_bytes(remaining[:11])
        parts = remaining[11:].split(None, 1)
        if len(parts) == 1:
            instruction = parts[0]
            arguments = None
        else:
            instruction, args_str = parts
            arguments = tuple(arg.strip() for arg in args_str.split(","))

        instructions.append(Instruction(raw_bytes, instruction, arguments))
        # Update for next iteration.
        offset += 4

    return instructions


def format_preamble(obj_path, n):
    if IS_LINUX:
        return DISASSEMBLED_PREAMBLE_LINUX.format(obj_path=obj_path, n=n)

    if IS_MACOS:
        return DISASSEMBLED_PREAMBLE_MACOS.format(obj_path=obj_path, n=n)

    raise RuntimeError("Unsupported Platform", sys.platform)


def generate_pow_assembly(n):
    fortran_src = F90_TEMPLATE.format(n=n)
    src_filename = "pow{n}.f90".format(n=n)
    obj_filename = "pow{n}.o".format(n=n)
    with tempfile.TemporaryDirectory() as dirname:
        src_path = os.path.join(dirname, src_filename)
        with open(src_path, "w") as file_obj:
            file_obj.write(fortran_src)

        obj_path = os.path.join(dirname, obj_filename)
        subprocess.check_output(
            ["gfortran", "-c", "-O3", src_path, "-o", obj_path, "-J", dirname]
        )
        dis_bytes = subprocess.check_output(
            ["objdump", "--disassemble", obj_path]
        )

    disassembled = dis_bytes.decode("ascii")
    preamble = format_preamble(obj_path, n)
    return parse_disassembled(disassembled, preamble)


def positive_int(value):
    """Helper for ``argparse`` to consume a positive integer.

    H/T: https://stackoverflow.com/a/14117511/1068170

    Args:
        value (str): The command line value. Expected to be a positive
            integer in string form.

    Returns:
        int: The parsed ``value``.

    Raises:
        argparse.ArgumentTypeError: If ``value`` cannot be parsed to
            an integer.
        argparse.ArgumentTypeError: If ``value`` **is** an integer but is
            non-positive.
    """
    try:
        as_int = int(value)
    except (ValueError, TypeError):
        msg = "{!r} cannot be converted to an integer".format(value)
        raise argparse.ArgumentTypeError(msg)

    if as_int <= 0:
        msg = "{:g} is not a positive integer".format(as_int)
        raise argparse.ArgumentTypeError(msg)

    return as_int


def get_exponent():
    parser = argparse.ArgumentParser(
        description="Generate assembly for `a**n` generated by `gfortran`",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--exponent",
        dest="n",
        default=5,
        type=positive_int,
        help="The exponent to use when generating assembly.",
    )

    args = parser.parse_args()
    return args.n


def _get_both_registers(instruction, name):
    if instruction.arguments is None or len(instruction.arguments) != 2:
        raise ValueError("Unexpected {} instruction".format(name), instruction)
    src_register = get_register(instruction.arguments[0])
    target_register = get_register(instruction.arguments[1])
    return src_register, target_register


def handle_movapd(register_history, instruction):
    src_register, target_register = _get_both_registers(instruction, "movapd")

    registers, _ = register_history[-1]
    if src_register not in registers:
        raise KeyError("Missing register", src_register)

    new_registers = {}
    new_registers.update(registers)
    new_registers[target_register] = new_registers[src_register]
    register_history.append((new_registers, instruction))


def handle_mulsd(register_history, instruction):
    src_register, target_register = _get_both_registers(instruction, "mulsd")

    registers, _ = register_history[-1]
    value1 = registers.get(src_register)
    if value1 is None:
        raise KeyError("Missing register", src_register)

    value2 = registers.get(target_register)
    if value2 is None:
        raise KeyError("Missing register", target_register)

    if value1 != VAR_NAME:
        value1 = "({})".format(value1)
    if value2 != VAR_NAME:
        value2 = "({})".format(value2)

    new_registers = {}
    new_registers.update(registers)
    new_registers[target_register] = "{} * {}".format(value1, value2)
    register_history.append((new_registers, instruction))


def show_register_history(register_history):
    widths = {}
    min_width = len(" %xmm0[:64] ")
    for registers, _ in register_history:
        for register, str_value in registers.items():
            curr_width = widths.get(register, min_width)
            # Add a buffer of 2 spaces on either side.
            widths[register] = max(curr_width, len(str_value) + 2)

    indices = sorted(widths.keys())
    # Print the headers and divider_parts.
    headers = [""]
    divider_parts = [""]
    for index in indices:
        named = "%xmm{:d}[:64]".format(index)
        # Add a buffer of 2 spaces on either side.
        headers.append(named.center(widths[index], " "))
        divider_parts.append("-" * widths[index])
    headers.append("")
    divider_parts.append("")
    divider = "+".join(divider_parts)
    print(divider)
    print("|".join(headers))
    print(divider)

    for registers, instruction in register_history:
        curr_row_parts = [""]
        for index in indices:
            str_value = registers.get(index, "")
            curr_row_parts.append(str_value.center(widths[index], " "))
        curr_row_parts.append("")
        curr_row = "|".join(curr_row_parts)
        print("{} {}".format(curr_row, pretty(instruction)))

    print(divider)


def track_exponentiation(n):
    instructions = generate_pow_assembly(n)
    input_register = get_input_register(instructions[0])

    register_history = [({input_register: VAR_NAME}, instructions[0])]
    for instruction in instructions[1:-2]:
        if instruction.name == MOVAPD:
            handle_movapd(register_history, instruction)
        elif instruction.name == MULSD:
            handle_mulsd(register_history, instruction)
        else:
            raise ValueError("Unexpected instruction", instruction)

    output_register = get_output_register(instructions[-2])
    register_history.append(({output_register: "b"}, instructions[-2]))

    verify_last_register(instructions[-1])

    # Now print the conclusions.
    show_register_history(register_history)


def main():
    n = get_exponent()
    track_exponentiation(n)


if __name__ == "__main__":
    main()
