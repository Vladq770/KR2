import numpy as np
from math import sqrt, exp
import matplotlib.pyplot as plt
from scipy import linalg


def psi_r(r, R):
    return 100 * np.exp(-(r / (0.1 * R)) ** 2)


def get_new_tridiag(old_tridiag, N):
    new_tridiag = np.zeros((1 + 1 + 1, N + 1))
    for j in range(N + 1):
        for i in range(N + 1):
            index = 1 + i - j
            if 0 <= index < 1 + 1 + 1:
                new_tridiag[index][j] = old_tridiag[i][j]
    return new_tridiag


def tridiag_alg(new_tridiag, d):
    ans = linalg.solve_banded((1, 1), new_tridiag, d)
    return ans


def tridiag(a, b, c, k1=-1, k2=0, k3=1):
    return np.diag(a, k1) + np.diag(b, k2) + np.diag(c, k3)


def get_eta(r_i, a2, t, h):
    eta_i = (a2 * t) / (4 * r_i * h)
    return eta_i


def get_d(v_t, theta, gamma, eta, N, u_c):
    d_temp = np.zeros(N + 1, dtype=np.float64)
    d_temp[0] = (1 - 2 * theta - gamma) * v_t[0] + 2 * theta * v_t[1] + 2 * gamma * u_c
    for i in range(1, N - 1):
        d_temp[i] = (1 - theta - gamma) * v_t[i] + (eta[i - 1] + theta / 2) * v_t[i + 1] + ((theta / 2) - eta[i - 1]) * \
                    v_t[i - 1] + 2 * gamma * u_c
    d_temp[N] = theta * v_t[N - 1] + (1 - theta - gamma) * v_t[N] + 2 * gamma * u_c
    return d_temp


def get_b(N, theta, gamma):
    b = np.zeros(N + 1, dtype=np.float64)
    b[0] = 1 + 2 * theta + gamma
    for i in range(1, N + 1):
        b[i] = 1 + theta + gamma
    return b


def get_a(N, theta, eta):
    a = np.zeros(N, dtype=np.float64)
    for i in range(N - 1):
        a[i] = - ((theta / 2) - eta[i])
    a[N - 1] = -theta
    return a


def get_c(N, theta, eta):
    c = np.zeros(N, dtype=np.float64)
    c[0] = -2 * theta
    for i in range(1, N):
        c[i] = - ((theta / 2) + eta[i - 1])
    return c


def get_old_tridiag(N, theta, gamma, eta_i):
    a = get_a(N, theta, eta_i)
    b = get_b(N, theta, gamma)
    c = get_c(N, theta, eta_i)
    old_tridiag = tridiag(a, b, c)
    return old_tridiag


def solve_schema2(coeff):
    N = int(coeff[10])
    K = int(coeff[9])
    l = coeff[1]
    R = coeff[0]
    u_c = coeff[2]
    alpha = coeff[3]
    k_ = coeff[5]
    c = coeff[6]
    h = R / N
    T = coeff[4]
    t = T / K
    a2 = k_ / c

    r_i = np.arange(0, R + h, h)[:N + 1]  # значения в узлах по r
    t_k = np.arange(0, T + t, t)[:K + 1]  # значение в узлах по t
    dist_k = len(t_k)  # количество узлов по t
    dist_i = len(r_i)  # количество узлов по r
    # w_h_t = np.zeros((dist_k, dist_i))  # итоговая сетка размером x_i*t_k

    # Тетта, этта, гамма для прогнонки
    theta = (a2 * t) / h ** 2
    gamma = (a2 * t * alpha) / (2 * l * k_)
    eta_i = get_eta(r_i[1:len(r_i) - 1], a2, t, h)

    #v_i_k = np.zeros(K + 1, dtype=object)
    v_i_k = np.empty((K + 1, N + 1))
    v_i_k[0] = psi_r(r_i, R)
    #d_i_k = np.zeros(K + 1, dtype=object)
    d_i_k = np.empty((K + 1, N + 1))
    d_temp = np.array(get_d(v_i_k[0], theta, gamma, eta_i, N, u_c))
    d_i_k[0] = d_temp
    old_tridiag = get_old_tridiag(N, theta, gamma, eta_i)
    new_tridiag = np.array(get_new_tridiag(old_tridiag, N))
    # print(new_tridiag)
    # print(type(new_tridiag[0]))
    # print(type(new_tridiag[0][0]))
    # print(d_temp)
    for s in range(K):
        # print(s)
        v_temp = tridiag_alg(new_tridiag, d_temp)
        v_i_k[s + 1] = v_temp
        d_temp = np.array(get_d(v_i_k[s + 1], theta, gamma, eta_i, N, u_c))
        d_i_k[s + 1] = d_temp
    return v_i_k