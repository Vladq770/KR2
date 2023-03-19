import math
from numpy import arange
from mpmath import *
from zeros import arr


## Нахождение нормы
def norma(rk):
    return 1 / ((j0(rk) ** 2))


## Нахождение значения подинтегральной функции
def func(r, rk, R):
    return exp(-(r / (0.1 * R)) ** 2) * j0(rk * r / R) * r


def integr(rk):
    return exp(-(rk ** 2 / 400))



def simpson_method(func, min_lim, max_lim, delta,rk):
    def integrate(func, min_lim, max_lim, n):
        integral = mpf(0)
        step = (max_lim - min_lim) / n
        for x in arange(min_lim + step / 2, max_lim - step / 2, step):
            integral += step / 6 * (func(x - step / 2, rk, max_lim) + 4 * func(x,rk, max_lim) + func(x + step / 2, rk, max_lim))
        return integral


    d, n = mpf(1), 1
    f1 = integrate(func, mpf(min_lim), mpf(max_lim), n * 2)
    f2 = integrate(func, mpf(min_lim), mpf(max_lim), n)
    while abs(d) > delta:
        d = (f1 - f2) / 15
        #print(type(d))
        #print(d)
        n *= 2
        f2 = f1
        f1 = integrate(func, min_lim, max_lim, n * 2)

    a = abs(f2)
    b = abs(f2) + d
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



def t0(r, R):
    return 100 * exp(-(r / (0.1 * R)) ** 2)




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



def n_theoretical(e, R, k, C, d):
    N = 1
    val = 1
    while(val > e):
        val = 3 / (0.01 + 4 / R**2 * k / C * d) * exp(-(N * pi)**2 * (1 / 400 + k / C / R**2 * d))
        #print(val)
        N += 1
    print(N)
    return N



def n_experimental(N, R, k, L, C, alpha, e, d):
    val = 0
    for i in range(1, N + 1):
        val += 1 / (j0(arr[i])**2 * exp(((arr[i] / R) ** 2 + alpha / (L * k)) * k / C * d) * exp(arr[i]**2 / 400))
        #print(val)
    temp = val
    while True:
        temp -= 1 / (j0(arr[N])**2 * exp(((arr[N] / R) ** 2 + alpha / (L * k)) * k / C * d) * exp(arr[N]**2 / 400))
        if(abs(temp - val) > e):
            break
        N -= 1
    print(N)
    return N



def integral0(Uc):

    val = 1 - exp(-100)
    return val - Uc



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
        #print("Номер N до", N)
        #print("Член ряда ", part)
    n = N
    while(part > e * 1e-6):
        part = f(N, tmin, R, k, C)
        val += part
        #print("Номер N ", N)
        #print("Член ряда ", part)
        N += 1
    if val > e:
        while(val > e):
            val -= f(n, tmin, R, k, C)
            n += 1
    return (val, n)



def calculation(coeff: list):
    t = int(log10((1 / coeff[8]) ** 2)) + 5
    if t < 15:
        t = 15
    print(t)
    mp.dps = t
    n = n_theoretical(coeff[8], coeff[0], coeff[5], coeff[6], coeff[7])
    N = n_experimental(n, coeff[0], coeff[5], coeff[1], coeff[6], coeff[3], coeff[8], coeff[7])
    C1 = integral0(coeff[2])
    print("N=", N)
    C2 = exp_0(coeff[3], coeff[1], coeff[5], coeff[6])
    C1k, C2k, C3k = [], [], []
    print(C1)
    for i in range(N + 1):
        C1k.append(arr[i] / coeff[0])
        #print("Норма", i, norma(arr[i], coeff[0]))
        #print(i, N, norma(arr[i], coeff[0]), simpson_method(func, 0, coeff[0], coeff[8], arr[i]))
        #C2k.append(norma(arr[i], coeff[0]) * simpson_method(func, 0, coeff[0], mpf(coeff[8]) ** 2, arr[i]))
        C2k.append(norma(arr[i]) * integr(arr[i]))
        #print("Симпсон", i, simpson_method(func, 0, coeff[0], mpf(coeff[8]) ** 2, arr[i]))
        C3k.append(exp_k(coeff[0], arr[i], coeff[3], coeff[1], coeff[5], coeff[6]))
    return C1, C2, C1k, C2k, C3k