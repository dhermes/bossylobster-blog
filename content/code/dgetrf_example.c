#include <stdio.h>

extern void dgetrf_(const int* M, const int* N, double* A, const int* LDA,
    int* IPIV, int* INFO);

void disp3x3(double* A)
{
    printf("  A = [% .2f, % .2f, % .2f]\n", A[0], A[3], A[6]);
    printf("      [% .2f, % .2f, % .2f]\n", A[1], A[4], A[7]);
    printf("      [% .2f, % .2f, % .2f]\n", A[2], A[5], A[8]);
}

int main()
{
    int M = 3;
    int N = 3;
    double A[9] = { 4, 0, 1, 4, 4, 1, -3, -1, 1 };
    int LDA = 3;
    int IPIV[3];
    int INFO;

    printf("Inputs: \n");
    printf("  M = %d\n", M);
    printf("  N = %d\n", N);
    disp3x3(A);
    printf("  LDA = %d\n", LDA);

    dgetrf_(&M, &N, A, &LDA, IPIV, &INFO);

    printf("Outputs:\n");
    disp3x3(A);
    printf("  IPIV = [%d, %d, %d]\n", IPIV[0], IPIV[1], IPIV[2]);
    printf("  INFO = %d\n", INFO);

    return 0;
}
