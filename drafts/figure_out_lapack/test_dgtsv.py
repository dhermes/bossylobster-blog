import numpy as np


def main():
    lower_diag = np.diag([-1, -2, -1, -1], k=-1)
    diag = np.diag([2, 2, 3, 3, 1], k=0)
    upper_diag = np.diag([-1, -1, -1, -2], k=1)
    A = np.array(lower_diag + diag + upper_diag, dtype=np.float64)

    b_rhs = np.array([[1, 2, 3, 2, 1]], dtype=np.float64).T

    x_lhs = np.linalg.solve(A, b_rhs)

    print A
    print b_rhs
    print x_lhs


if __name__ == '__main__':
    main()
