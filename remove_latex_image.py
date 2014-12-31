#!/usr/bin/env python
import json
import subprocess
import sys


LATEX_EQUATION_NUMBERS_FILE = 'latex_equation_numbers.json'
with open(LATEX_EQUATION_NUMBERS_FILE, 'r') as fh:
    EQUATION_NUMBERS = json.load(fh)


def remove_key_from_cache(equation_number):
    matches = [key for key, value in EQUATION_NUMBERS.iteritems()
               if value == equation_number]
    if len(matches) != 1:
        raise ValueError((equation_number, 'Not found exactly once.'))
    matching_key = matches[0]
    EQUATION_NUMBERS.pop(matching_key)
    with open(LATEX_EQUATION_NUMBERS_FILE, 'w') as fh:
        json.dump(EQUATION_NUMBERS, fh, indent=2, sort_keys=True,
                  separators=(',', ': '))
        fh.write('\n')


def remove_image_file(equation_number):
    filename = 'content/latex_images/%d.svg' % (equation_number,)
    subprocess.call(['git', 'rm', filename])


def remove_image(equation_number):
    remove_key_from_cache(equation_number)
    remove_image_file(equation_number)


def main(argv):
    equation_number = None
    if len(argv) == 2:
        try:
            equation_number = int(argv[1])
        except (TypeError, ValueError):
            pass

    if equation_number is None:
        print >> sys.stderr, 'Usage:'
        print >> sys.stderr, '    remove_latex_image.py EQUATION_NUMBER'
        sys.exit(1)

    remove_image(equation_number)


if __name__ == '__main__':
    main(sys.argv)
