# Helper for 2016-11-25-newtons-failure

import os

import matplotlib.pyplot as plt
import numpy as np
import seaborn


seaborn.set_palette('husl')


CURR_DIR = os.path.dirname(__file__)
IMAGES_DIR = os.path.join(CURR_DIR, 'content', 'images')


def add_line(x_val):
    dfx = 2.0 * (x_val - 1.0)
    fx = dfx * dfx * 0.25

    # Also add points off the graph.
    # y = fx + dfx (x - x_val)
    left_x = -1.0
    left_y = fx + dfx * (left_x - x_val)
    right_x = 3.0
    right_y = fx + dfx * (right_x - x_val)
    plt.plot([left_x, x_val, right_x],
             [left_y, fx, right_y], alpha=0.5, marker='o')

    new_x = x_val - fx / dfx
    new_fx = (new_x - 1.0) * (new_x - 1.0)
    plt.plot([new_x, new_x], [0.0, new_fx],
             linestyle='dashed', color='black', alpha=0.5)


def main():
    x_values = np.linspace(-0.5, 2.5, 512)
    y_values = (x_values - 1.0) * (x_values - 1.0)
    plt.plot(x_values, y_values)

    add_line(2.0)
    add_line(1.5)
    add_line(1.25)
    add_line(1.125)
    add_line(1.0625)

    plt.axis('scaled')
    plt.xlim(-0.625, 2.625)
    plt.ylim(-0.125, 2.5)
    filename = 'newton_at_work.png'
    full_path = os.path.join(IMAGES_DIR, filename)
    plt.savefig(full_path, bbox_inches='tight')
    print('Saved {}'.format(filename))


if __name__ == '__main__':
    main()
