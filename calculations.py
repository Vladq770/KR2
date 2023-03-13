import math
from numpy import arange
from mpmath import j1, j0
from zeros import arr


## Нахождение нормы
def norma(rk, R):
    return 2 / (R ** 2 * (j(rk, 0, 10000) ** 2))


## Нахождение значения подинтегральной функции
def func(r, rk, R):
    return 100 * math.exp(-(r / (0.1 * R)) ** 2) * j(rk * r / R, 0, 10000) * r



def simpson_method(func, min_lim, max_lim, delta,rk):
    def integrate(func, min_lim, max_lim, n):
        integral = 0.0
        step = (max_lim - min_lim) / n
        for x in arange(min_lim + step / 2, max_lim - step / 2, step):
            integral += step / 6 * (func(x - step / 2, rk, max_lim) + 4 * func(x,rk, max_lim) + func(x + step / 2, rk, max_lim))
        return integral

    d, n = 1, 1
    while abs(d) > delta:
        d = (integrate(func, min_lim, max_lim, n * 2) - integrate(func, min_lim, max_lim, n)) / 15
        n *= 2

    a = abs(integrate(func, min_lim, max_lim, n))
    b = abs(integrate(func, min_lim, max_lim, n)) + d
    if a > b:
        a, b = b, a
    return a


## Нахождение значения Jn
def j(x, n, steps):
    """if steps < int(x):
        steps = int(x)
    val = 0
    for i in range(1, steps):
        val += (math.cos(n * i * math.pi / steps - x * math.sin(i * math.pi / steps)))
    val += (math.cos(n * 0 - x * math.sin(0)) + math.cos(n * math.pi - x * math.sin(math.pi))) / 2
    return val / steps"""
    return float(j0(x))



## Метод дихотомии для нахождения нулей
def dih(a, b, e, n, steps):
    while((b - a) / 2 > e):
        c = (a + b) / 2
        c_val = j(c, n, steps)
        if c_val == 0:
            return c_val
        if (j(a, n, steps) * c_val < 0):
            b = c
        else:
            a = c
    return (a + b) / 2



## Нахождение нулей J1
def zeros_of_J1(arr, steps, N, e):
    for i in range(N+1):
        c = arr[len(arr) - 1]
        arr.append(dih(c + math.pi-0.1, c + math.pi+0.1, e, 1, steps))




def exp_k(R, rk, alpha, L, k, C):
    lambda_k = (rk / R) ** 2 + alpha / (L * k)
    return lambda_k * k / C


def f0(r, R):
    return 100 * math.exp(-(r / (0.1 * R)) ** 2) * r


def integral0(R, steps, Uc):
    val = 0
    for i in range(1, steps):
        val += f0(i / R, R) * (R / steps)
    val += (f0(0, R) + f0(R, R)) * (R / steps) / 2
    return val * 2 / R ** 2 - Uc



def exp_0(alpha, L, k, C):
    lambda_k = alpha / (L * k)
    return lambda_k * k / C



def row_k(n, tmin, R, k, C):
    k = math.floor(((math.pi * n / R) ** 2) * tmin * k / C)
    return math.pi ** 2 * (n + 1/2) / (2 ** k)



def row_sum(f, N, e, tmin, R, k, C):
    val = 0
    part = 1
    while(part > e):
        part = f(N, tmin, R, k, C)
        N += 1
        print("Номер N до", N)
        print("Член ряда ", part)
    n = N
    while(part > e * 1e-6):
        part = f(N, tmin, R, k, C)
        val += part
        print("Номер N ", N)
        print("Член ряда ", part)
        N += 1
    if val > e:
        while(val > e):
            val -= f(n, tmin, R, k, C)
            n += 1
    return (val, n)



def calculation(coeff: list):
    val, N = row_sum(row_k, 1, coeff[8], coeff[7], coeff[0], coeff[5], coeff[6])
    print(val, N)
    if N > len(arr):
        zeros_of_J1(arr, 10000, N - len(arr), 1e-6)
    C1 = integral0(coeff[0], 10000, coeff[2])
    C2 = exp_0(coeff[3], coeff[1], coeff[5], coeff[6])
    C1k, C2k, C3k = [], [], []
    for i in range(N):
        C1k.append(arr[i] / coeff[0])
        #print("Норма", i, norma(arr[i], coeff[0]))
        #print("Симпсон", i, simpson_method(func, 0, coeff[0], coeff[8], arr[i]))
        #print(i, N, norma(arr[i], coeff[0]), simpson_method(func, 0, coeff[0], coeff[8], arr[i]))
        C2k.append(norma(arr[i], coeff[0]) * simpson_method(func, 0, coeff[0], coeff[8], arr[i]))
        C3k.append(exp_k(coeff[0], arr[i], coeff[3], coeff[1], coeff[5], coeff[6]))
    return C1, C2, C1k, C2k, C3k