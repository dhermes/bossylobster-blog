import os
import pathlib

import matplotlib  # matplotlib==3.7.2
import matplotlib.pyplot as plt  # matplotlib==3.7.2
import mpmath  # mpmath==1.3.0
import numpy as np  # numpy==1.24.3
import seaborn  # seaborn==0.12.2
import sympy  # sympy==1.12


HERE = pathlib.Path(__file__).resolve().parent
_COLORS = seaborn.color_palette(palette="deep", n_colors=6)
BLUE = _COLORS[0]
GREEN = _COLORS[2]


def part1():
    n, s, X = sympy.symbols("n, s, X")
    f = 1 + n * (n - 1) / 2 + n * (n - 1) * (n - 2) * (n - 3) / 24
    g = 24 * f - 1 / X**4
    gs = (g.subs({n: s / X}) * X**4).expand()
    print("g(s) =", gs)
    g2 = gs.diff(s, 2)
    g2 = (g2 - 19 * X**2).factor() + 19 * X**2
    print("g''(s) =", g2)
    print("g(0) =", gs.subs({s: 0}))

    lower_half = gs.subs({s: 1 + sympy.Rational(1, 2) * X}).expand()
    lower_one = gs.subs({s: 1 + X}).expand()
    lower_46 = gs.subs({s: 1 + sympy.Rational(146, 100) * X}).expand()
    upper = gs.subs({s: 1 + sympy.Rational(3, 2) * X}).expand()
    print("g(1 + 0.5X) =", lower_half)
    print("g(1 + X) =", lower_one)
    print("g(1 + 1.46X) =", lower_46)
    print("g(1 + 1.5X) =", upper)

    print("-" * 40)
    alpha = sympy.Function("alpha")(X)
    implicit = gs.subs({s: alpha})
    print("0 =", implicit)
    print("0 =", implicit.subs({X: 0}))

    implicit1 = implicit.diff(X)
    alpha0 = alpha.subs({X: 0})
    print("0 =", implicit1.subs({X: 0}).factor())
    print("0 =", implicit1.subs({X: 0}).subs({alpha0: 1}))

    implicit2 = implicit.diff(X, 2)
    alpha_prime = sympy.diff(alpha, X)
    alpha_prime0 = alpha_prime.subs({X: 0})
    print("0 =", implicit2.subs({X: 0}))
    print(
        "0 =",
        implicit2.subs({X: 0}).subs({alpha0: 1, alpha_prime0: sympy.Rational(3, 2)}),
    )


def lower_bound_half(x_value):
    return (
        321.0 * x_value**4 / 16.0
        + x_value**3
        + 31.0 * x_value**2 / 2.0
        - 4.0 * x_value
    )


def lower_bound_one(x_value):
    return (
        24.0 * x_value**4 + 14.0 * x_value**3 + 11.0 * x_value**2 - 2.0 * x_value
    )


def lower_bound_46(x_value):
    return (
        203860641.0 * x_value**4 / 6250000.0
        + 363121.0 * x_value**3 / 15625.0
        + 11887.0 * x_value**2 / 1250.0
        - 4.0 * x_value / 25.0
    )


def upper_bound(x_value):
    return 537.0 * x_value**4 / 16.0 + 24.0 * x_value**3 + 19.0 * x_value**2 / 2.0


def part2_plot1(ax):
    x_start, x_end = -0.25, 0.5
    X_values = np.linspace(x_start, x_end, 1025)
    Y_values = lower_bound_half(X_values)

    ax.plot(X_values, Y_values, color=BLUE)
    ax.plot([x_start, x_end], [0.0, 0.0], color="black", linestyle="dashed")

    for m in range(2, 6):
        X_value = np.sqrt(np.sqrt(1.0 / (24 * 2**m)))
        Y_value = lower_bound_half(X_value)
        ax.plot(X_value, Y_value, color=GREEN, marker="o", linestyle="none")
        ax.text(X_value + 0.015, Y_value - 0.02, f"$m = {m}$", fontsize=10)

    ax.plot(0.0, 0.0, color=GREEN, marker="o", linestyle="none")

    ax.set_xlim(-0.015625, 0.390625)
    ax.set_ylim(-0.375, 1.125)

    ax.set_xlabel("$X$", fontsize=12)
    ax.set_title(r"$g\left(1 + \frac{1}{2} X; X\right)$", fontsize=16)


def part2_plot2(ax):
    x_start, x_end = -0.25, 0.5
    X_values = np.linspace(x_start, x_end, 1025)
    Y_values = lower_bound_one(X_values)

    ax.plot(X_values, Y_values, color=BLUE)
    ax.plot([x_start, x_end], [0.0, 0.0], color="black", linestyle="dashed")

    for m in range(5, 9):
        X_value = np.sqrt(np.sqrt(1.0 / (24 * 2**m)))
        Y_value = lower_bound_one(X_value)
        ax.plot(X_value, Y_value, color=GREEN, marker="o", linestyle="none")
        ax.text(X_value + 0.01, Y_value - 0.01, f"$m = {m}$", fontsize=10)

    ax.plot(0.0, 0.0, color=GREEN, marker="o", linestyle="none")

    ax.set_xlim(-0.015625, 0.265625)
    ax.set_ylim(-0.125, 0.53125)

    ax.set_xlabel("$X$", fontsize=12)
    ax.set_title(r"$g\left(1 + X; X\right)$", fontsize=16)


def part2_plot3(ax):
    x_start, x_end = -0.5, 0.5
    X_values = np.linspace(x_start, x_end, 1025)
    Y_values = lower_bound_46(X_values)

    ax.plot(X_values, Y_values, color=BLUE)
    ax.plot([x_start, x_end], [0.0, 0.0], color="black", linestyle="dashed")

    for m in range(18, 22):
        X_value = np.sqrt(np.sqrt(1.0 / (24 * 2**m)))
        Y_value = lower_bound_46(X_value)
        ax.plot(X_value, Y_value, color=GREEN, marker="o", linestyle="none")
        if m == 19 or m == 20:
            ax.text(X_value + 0.001, Y_value, f"$m = {m}$", fontsize=10)
        else:
            ax.text(X_value + 0.001, Y_value - 0.0001, f"$m = {m}$", fontsize=10)

    ax.plot(0.0, 0.0, color=GREEN, marker="o", linestyle="none")

    ax.set_xlim(-0.0015625, 0.0328125)
    ax.set_ylim(-0.00095, 0.005)

    ax.set_xlabel("$X$", fontsize=12)
    ax.set_title(r"$g\left(1 + 1.46 X; X\right)$", fontsize=16)


def part3_plot1(ax):
    x_start, x_end = -0.5, 1.0
    X_values = np.linspace(x_start, x_end, 1025)
    Y_values = upper_bound(X_values)

    ax.plot(X_values, Y_values, color=BLUE)
    ax.plot([x_start, x_end], [0.0, 0.0], color="black", linestyle="dashed")
    ax.plot(0.0, 0.0, color=GREEN, marker="o", linestyle="none")

    ax.set_xlim(-0.03125, 0.53125)
    ax.set_ylim(-0.625, 9)

    ax.set_xlabel("$X$", fontsize=12)
    ax.set_title(r"$g\left(1 + \frac{3}{2} X; X\right)$", fontsize=16)


def part2():
    figure, all_axes = plt.subplots(1, 3)
    all_axes = all_axes.flatten()
    ax1, ax2, ax3 = all_axes
    part2_plot1(ax1)
    part2_plot2(ax2)
    part2_plot3(ax3)

    figure.set_size_inches(19.2, 4.8)
    figure.savefig(HERE / "moser-lower-bounds.pdf", bbox_inches="tight")
    figure.savefig(HERE / "moser-lower-bounds.png", bbox_inches="tight")
    plt.close(figure)


def part3():
    figure = plt.figure()
    ax = figure.gca()
    part3_plot1(ax)
    figure.savefig(HERE / "moser-upper-bound.pdf", bbox_inches="tight")
    figure.savefig(HERE / "moser-upper-bound.png", bbox_inches="tight")
    plt.close(figure)


def guess_floor(ctx, m):
    radical = ctx.sqrt(ctx.sqrt(24 * 2**m))
    if radical + 1.5 == radical:
        raise RuntimeError("Context is out of precision", m)
    return int(ctx.floor(radical + 1.5))


def integer_contained_46(ctx, m):
    upper = guess_floor(ctx, m)

    radical = ctx.sqrt(ctx.sqrt(24 * 2**m))
    lower = int(ctx.ceil(radical + 1.46))
    if lower == upper:
        return lower

    return None


def contains_integer_46(ctx, m):
    return integer_contained_46(ctx, m) is not None


def part4():
    ctx = mpmath.MPContext()
    ctx.prec = 500

    contains_count = 0
    for_plotting = []
    for m in range(20, 20 + 1600):
        if contains_integer_46(ctx, m):
            contains_count += 1
        for_plotting.append((m, contains_count))

    figure = plt.figure()
    ax = figure.gca()

    for_plotting = np.array(for_plotting)
    m_values = for_plotting[:, 0]
    ax.plot(
        m_values,
        0.04 * m_values,
        label="$(1.5 - 1.46)m$",
        color="black",
        linestyle="dashed",
    )
    ax.plot(m_values, for_plotting[:, 1], label="$C_{1.46}(m)$")
    ax.legend(loc="lower right", fontsize=12)
    ax.set_xlabel("$m$")

    figure.savefig(HERE / "moser-integers-in-window.pdf", bbox_inches="tight")
    figure.savefig(HERE / "moser-integers-in-window.png", bbox_inches="tight")
    plt.close(figure)


def part5():
    ctx = mpmath.MPContext()
    ctx.prec = 500

    for m in range(20, 20 + 1600):
        guess = integer_contained_46(ctx, m)
        if guess is None:
            continue

        numerator = 24 * (2**m - 1)
        remainder = numerator % guess
        if remainder == 0:
            print(m, guess)


def part6():
    print("-" * 40)
    ctx = mpmath.MPContext()
    ctx.prec = 500

    for m in range(4, 4 + 1600):
        guess = guess_floor(ctx, m)
        numerator = 24 * (2**m - 1)
        remainder = numerator % guess
        if remainder == 0:
            print(m, guess)


def part7():
    figure = plt.figure()
    ax = figure.gca()
    part2_plot1(ax)

    figure.savefig(HERE / "moser-lower-bound-01.pdf", bbox_inches="tight")
    figure.savefig(HERE / "moser-lower-bound-01.png", bbox_inches="tight")
    plt.close(figure)


def part8():
    figure = plt.figure()
    ax = figure.gca()
    part2_plot3(ax)

    figure.savefig(HERE / "moser-lower-bound-02.pdf", bbox_inches="tight")
    figure.savefig(HERE / "moser-lower-bound-02.png", bbox_inches="tight")
    plt.close(figure)


def main():
    # $ brew install texlive
    # $ brew install --cask tex-live-utility
    # $ sudo tlmgr install cm-super
    os.environ["SOURCE_DATE_EPOCH"] = "0"
    matplotlib.rcParams["text.usetex"] = True
    matplotlib.rcParams["mathtext.rm"] = "serif"
    matplotlib.rcParams["mathtext.fontset"] = "cm"
    seaborn.set_theme()
    part1()
    part2()
    part3()
    part4()
    part5()
    part6()
    part7()
    part8()


if __name__ == "__main__":
    main()
