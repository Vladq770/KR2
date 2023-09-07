import numpy as np
from numpy import linalg as la
import math


def psi(r, R):
    return 100 * math.exp(-(r/(0.1*R)) ** 2)


def get_3diag_matr(I, a2, ht, hr, b):
    A = np.zeros((I + 1, I + 1))
    A[0, 0] = 1 + 4*a2*ht/(hr**2)+b*a2*ht
    A[0, 1] = -4*a2*ht/(hr**2)
    A[I, I-1] = -2*a2*ht/(hr**2)
    A[I, I] = 1 + 2*a2*ht/(hr**2)+b*a2*ht
    for i in range(I-1):
        A[i+1, i] = a2*ht/(2*hr*(i+1)*hr) - a2*ht/(hr**2)
        A[i+1, i+1] = 1 + 2*a2*ht/(hr**2)+b*a2*ht
        A[i+1, i+2] = -a2*ht/(2*hr*(i+1)*hr) - a2*ht/(hr**2)
    return A


def get_right_part(uk, I, alpha, uc, a2, ht, l, k):
    B = np.zeros((I + 1, 1))
    for i in range(I+1):
        B[i, 0] = uk[i, 0] + alpha*uc*a2*ht/(l*k)
    return B


def get_solve(A, B, u0, K, I, alpha, uc, a2, ht, l, k):
    res = np.zeros((K+1, I+1))
    res[0,:] = u0.reshape((1, I+1))
    for i in range(1, K+1):
        uk = la.solve(A, B)
        res[i,:] = uk.reshape((1, I+1))
        B = get_right_part(uk, I, alpha, uc, a2, ht, l, k)
    return res


def solve_schema1(coeff):
    K = int(coeff[9])
    I = int(coeff[10])
    hr = coeff[0] / I
    ht = coeff[4] / K
    R = coeff[0]
    l = coeff[1]
    uc = coeff[2]
    alpha = coeff[3]
    T = coeff[4]
    k = coeff[5]
    c = coeff[6]
    a2 = k / c
    b = alpha / (l * k)
    A = get_3diag_matr(I, a2, ht, hr, b)
    u0 = np.zeros((I + 1, 1))
    for i in range(I + 1):
        u0[i, 0] = psi(i * hr, R)
    B = get_right_part(u0, I, alpha, uc, a2, ht, l, k)
    Solve = get_solve(A, B, u0, K, I, alpha, uc, a2, ht, l, k)
    return Solve