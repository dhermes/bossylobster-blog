/* testlapack.c - test program for the LAPACK dgtsv function
 *
 * Copyright (C) 2004  Jochen Voss.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * $Id: testdgtsv.c 5702 2004-05-12 21:13:41Z voss $
 */

#include <stdio.h>

/* Understanding DGTSV:
   http://www.math.utah.edu/software/lapack/lapack-d/dgtsv.html
   http://www.netlib.org/clapack/CLAPACK-3.1.1/SRC/dgtsv.c */

double lowerDiag[] = {
  -1, -2, -1, -1
};

double diag[] = {
  2, 2, 3, 3, 1
};

double upperDiag[] = {
  -1, -1, -1, -2
};

double bForRHS[] = {
  1, 2, 3, 2, 1
};

// http://stackoverflow.com/questions/15830913
extern "C" void dgtsv_(const long *Np, const long *NRHSp, double *DL,
                       double *D, double *DU, double *B, const long *LDBp,
                       long *INFOp);

static long dgtsv(long N, long NRHS, double *DL, double *D, double *DU,
                  double *B, long LDB)
{
  long info;
  dgtsv_(&N, &NRHS, DL, D, DU, B, &LDB, &info);
  return info;
}

int
main()
{
  int i, info;
  long N = 5;

  printf("B for RHS before:\n");
  for (i=0; i<N; ++i) printf("%5.1f\n", bForRHS[i]);

  printf("Lower diag before:\n");
  for (i=0; i<N; ++i) printf("%5.1f\n", lowerDiag[i]);

  printf("==========\n==========\n==========\n");

  long NRHS = 1;
  long LDB = N;
  info = dgtsv(N, NRHS, lowerDiag, diag, upperDiag, bForRHS, LDB);
  if (info != 0) fprintf(stderr, "failure with error %d\n", info);

  printf("B for RHS after:\n");
  for (i=0; i<N; ++i) printf("%5.1f\n", bForRHS[i]);

  printf("Lower diag after:\n");
  for (i=0; i<N; ++i) printf("%5.1f\n", lowerDiag[i]);

  return 0;
}


// 1. solve the equation   A*X = B,
// 2. ...where A is an N-by-N tridiagonal matrix
// 3. Arguments
// ---- N : order of A
// ---- NRHS : number of columns of B (# RHS)
// ---- DL : diagonal lower (the first subdiagonal); N - 1 length array

/* On exit, DL is overwritten by the (n-2) */
/* elements of the second superdiagonal of the upper */
/* triangular matrix U from the LU factorization of A, */
/* in DL(1), ..., DL(n-2). */

// ---- D : diagonal; N length array
// ---- DU : diagonal upper (the first superdiagonal); N - 1 length array
// ---- B : the RHS matrix, expect it to be N x NRHS array in 2D

 /* On entry, the N-by-NRHS right hand side matrix B. */
 /* On exit, if INFO = 0, the N-by-NRHS solution matrix */

// ---- LDB : Leading dimension of B, LDB >= max(1, N)
// ---- INFO : exit code

// 4.
