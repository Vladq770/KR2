import numpy as np
import math
def psi(r, R):
    return 100 * math.exp(-(r/(0.1*R)) ** 2)

def solve_schema3(coeff):
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
    gamma = a2*ht/(hr ** 2)
    C0 = alpha*uc*a2*ht/(l*k)
    keff2 = 1 - 2*gamma - a2*ht*alpha/(l*k)
    keff3 = 1 - 4*gamma - a2*ht*alpha/(l*k)

    gamma_2 = a2 * (ht/2) / (hr ** 2)
    C0_2 = alpha * uc * a2 * (ht/2) / (l * k)
    keff2_2 = 1 - 2 * gamma_2 - a2 * (ht/2) * alpha / (l * k)
    keff3_2 = 1 - 4 * gamma_2 - a2 * (ht/2) * alpha / (l * k)
    def explicit():
        res = np.zeros((K + 1, I + 1))
        for i in range(I + 1):
            res[0, i] = psi(i * hr, R)
        for k in range(1, K + 1):
            for i in range(1, I):
                res[k, i] = res[k - 1, i - 1] * (gamma - gamma/(2*i)) + res[k - 1, i] * keff2 + res[k - 1, i + 1] * (gamma + gamma/(2*i)) + C0
            res[k, 0] = res[k - 1, 0] * keff3 + res[k - 1, 1] * (4*gamma) + C0
            res[k, I] = res[k - 1, I] * keff2 + res[k - 1, I - 1] * (2*gamma) + C0
        return res
    def explicit_2():

        res = np.zeros((2*K + 1, I + 1))
        for i in range(I + 1):
            res[0, i] = psi(i * hr, R)
        for k in range(1, 2*K + 1):
            for i in range(1, I):
                res[k, i] = res[k - 1, i - 1] * (gamma_2 - gamma_2/(2*i)) + res[k - 1, i] * keff2_2 + res[k - 1, i + 1] * (gamma_2 + gamma_2/(2*i)) + C0_2
            res[k, 0] = res[k - 1, 0] * keff3_2 + res[k - 1, 1] * (4*gamma_2) + C0_2
            res[k, I] = res[k - 1, I] * keff2_2 + res[k - 1, I - 1] * (2*gamma_2) + C0_2
        return res
    res1 = explicit()
    res2 = explicit_2()
    for k in range(K+1):
        res1[k,:] = -res1[k,:] + 2*res2[2*k,:]
    # print(res1)
    return res1


def solve_schema0(coeff):
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
    gamma = a2*ht/(hr ** 2)
    C0 = alpha*uc*a2*ht/(l*k)
    keff2 = 1 - 2*gamma - a2*ht*alpha/(l*k)
    keff3 = 1 - 4*gamma - a2*ht*alpha/(l*k)

    def explicit():
        res = np.zeros((K + 1, I + 1))
        for i in range(I + 1):
            res[0, i] = psi(i * hr, R)
        for k in range(1, K + 1):
            for i in range(1, I):
                res[k, i] = res[k - 1, i - 1] * (gamma - gamma/(2*i)) + res[k - 1, i] * keff2 + res[k - 1, i + 1] * (gamma + gamma/(2*i)) + C0
            res[k, 0] = res[k - 1, 0] * keff3 + res[k - 1, 1] * (4*gamma) + C0
            res[k, I] = res[k - 1, I] * keff2 + res[k - 1, I - 1] * (2*gamma) + C0
        return res

    return explicit()
