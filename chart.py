from calculations import calculation, t0
from explicit_schema import solve_schema0, solve_schema3
from implicit_schema import solve_schema1
from Crank_Nicholson_schema import solve_schema2
from mpmath import *
import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
import matplotlib.pyplot as plt
import numpy as np

mpl.use('TkAgg')
scheme = [solve_schema0, solve_schema1, solve_schema2, solve_schema3]
def chart(coeff: list, window):
    C1, C2, C1k, C2k, C3k = calculation(coeff)
    K = int(coeff[9])
    I = int(coeff[10])
    s_k = int(coeff[11])
    s_i = int(coeff[12])
    hr = coeff[0] / I
    ht = coeff[4] / K
    s_t = int(coeff[11]) * ht
    s_r = int(coeff[12]) * hr
    if coeff[13] == 4:
        tr = [i * ht for i in range(K + 1)]
        rt = [i * hr for i in range(I + 1)]
        print("rt", rt)
        print(len(rt))
        print("tr", tr)
        print(len(tr))
        tt = [s_k * ht]
        rr = [s_i * hr]
        Vt = []
        Vr = [[]]
        if s_k == 0:
            for i in rt:
                Vt.append(t0(i, coeff[0]))
        else:
            for j in rt:
                val = 0
                for k in range(1, len(C1k)):
                    x = j0(C1k[k] * j) * C2k[k] / exp((C3k[k] * s_t))
                    val += x
                Vt.append(val)
            for j in range(len(rt)):
                Vt[j] += coeff[2] + C1 / exp(C2 * s_t)

        for i in range(len(rr)):
            Vr[i].append(t0(rr[i], coeff[0]))
        for i in range(len(rr)):
            for j in range(1, len(tr)):
                val = 0
                for k in range(1, len(C1k)):
                    val += j0(C1k[k] * rr[i]) * C2k[k] / exp((C3k[k] * tr[j]))
                Vr[i].append(val)
        for i in range(len(rr)):
            for j in range(1, len(tr)):
                Vr[i][j] += coeff[2] + C1 / exp(C2 * tr[j])
        print('VT', Vt)
        print(len(Vt))
        print('VR', Vr)
        print(len(Vr))
        runge = scheme[3](coeff)
        no_runge = scheme[0](coeff)
        plt3(window, Vt, rt, tt, Vr, rr, tr, s_i, s_k, runge, no_runge)
        return
    if coeff[13] == 5:
        K_factor = 2
        I_factor = 2
        K_arr = [K]
        I_arr = [I]
        for i in range(3):
            K_arr.append(K_arr[-1] * K_factor)
            I_arr.append(I_arr[-1] * I_factor)
        schema_solve_ya = []
        schema_solve_r = []
        for i in range(len(K_arr)):
            coeff[9] = K_arr[i]
            coeff[10] = I_arr[i]
            schema_solve_ya.append(scheme[0](coeff))
            schema_solve_r.append(scheme[3](coeff))
        tt = [s_k * ht]
        rr = [s_i * hr]
        tr_arr = []
        rt_arr = []
        for i in range(len(K_arr)):
            ht_i = coeff[4] / K_arr[i]
            hr_i = coeff[0] / I_arr[i]
            tr_arr.append([j * ht_i for j in range(K_arr[i] + 1)])
            rt_arr.append([j * hr_i for j in range(I_arr[i] + 1)])
        ht_i = coeff[4] / K_arr[-1]
        hr_i = coeff[0] / I_arr[-1]
        tr = [i * ht_i for i in range(K_arr[-1] + 1)]
        rt = [i * hr_i for i in range(I_arr[-1] + 1)]
        print("rt", rt)
        print(len(rt))
        print("tr", tr)
        print(len(tr))
        Vt = []
        Vr = [[]]
        if s_k == 0:
            for i in rt:
                Vt.append(t0(i, coeff[0]))
        else:
            for j in rt:
                val = 0
                for k in range(1, len(C1k)):
                    x = j0(C1k[k] * j) * C2k[k] / exp((C3k[k] * s_t))
                    val += x
                Vt.append(val)
            for j in range(len(rt)):
                Vt[j] += coeff[2] + C1 / exp(C2 * s_t)

        for i in range(len(rr)):
            Vr[i].append(t0(rr[i], coeff[0]))
        for i in range(len(rr)):
            for j in range(1, len(tr)):
                val = 0
                for k in range(1, len(C1k)):
                    val += j0(C1k[k] * rr[i]) * C2k[k] / exp((C3k[k] * tr[j]))
                Vr[i].append(val)
        for i in range(len(rr)):
            for j in range(1, len(tr)):
                Vr[i][j] += coeff[2] + C1 / exp(C2 * tr[j])
        print('VT', Vt)
        print(len(Vt))
        print('VR', Vr)
        print(len(Vr))
        plt4(window, Vt, rt, tt, Vr, rr, tr, s_i, s_k, schema_solve_ya, schema_solve_r, tr_arr, rt_arr, K_arr, I_arr, K_factor, I_factor)
        return
    if coeff[14] == 0:
        schema_solve = scheme[coeff[13]](coeff)
        tr = [i * ht for i in range(K + 1)]
        rt = [i * hr for i in range(I + 1)]
        tt = tr
        rr = rt
        Vt = [[] for i in range(len(tr))]
        Vr = [[] for i in range(len(rt))]
        for i in range(len(rt)):
            Vt[0].append(t0(rt[i], coeff[0]))
            print("len Vt[0]", len(Vt[0]))
        for i in range(1, len(tt)):
            for j in range(len(rt)):
                val = 0
                for k in range(1, len(C1k)):
                    x = j0(C1k[k] * rt[j]) * C2k[k] / exp((C3k[k] * tt[i]))
                    val += x
                Vt[i].append(val)
        for i in range(1, len(tt)):
            for j in range(len(rt)):
                Vt[i][j] += coeff[2] + C1 / exp(C2 * tt[i])

        for i in range(len(rr)):
            Vr[i].append(t0(rr[i], coeff[0]))
        for i in range(len(rr)):
            for j in range(1, len(tr)):
                val = 0
                for k in range(1, len(C1k)):
                    val += j0(C1k[k] * rr[i]) * C2k[k] / exp((C3k[k] * tr[j]))
                Vr[i].append(val)
        for i in range(len(rr)):
            for j in range(1, len(tr)):
                Vr[i][j] += coeff[2] + C1 / exp(C2 * tr[j])

        plt0(window, Vt, rt, tt, Vr, rr, tr, s_i, s_k, schema_solve)
    elif coeff[14] == 1:
        K_factor = 2
        I_factor = 2
        if coeff[13] < 2:
            K_factor = 4
        K_arr = [K]
        I_arr = [I]
        for i in range(3):
            K_arr.append(K_arr[-1] * K_factor)
            I_arr.append(I_arr[-1] * I_factor)
        schema_solve = []
        for i in range(len(K_arr)):
            coeff[9] = K_arr[i]
            coeff[10] = I_arr[i]
            schema_solve.append(scheme[coeff[13]](coeff))
        tt = [s_k * ht]
        rr = [s_i * hr]
        tr_arr = []
        rt_arr = []
        for i in range(len(K_arr)):
            ht_i = coeff[4] / K_arr[i]
            hr_i = coeff[0] / I_arr[i]
            tr_arr.append([j * ht_i for j in range(K_arr[i] + 1)])
            rt_arr.append([j * hr_i for j in range(I_arr[i] + 1)])
        ht_i = coeff[4] / K_arr[-1]
        hr_i = coeff[0] / I_arr[-1]
        tr = [i * ht_i for i in range(K_arr[-1] + 1)]
        rt = [i * hr_i for i in range(I_arr[-1] + 1)]
        print("rt", rt)
        print(len(rt))
        print("tr", tr)
        print(len(tr))
        Vt = []
        Vr = [[]]
        if s_k == 0:
            for i in rt:
                Vt.append(t0(i, coeff[0]))
        else:
            for j in rt:
                val = 0
                for k in range(1, len(C1k)):
                    x = j0(C1k[k] * j) * C2k[k] / exp((C3k[k] * s_t))
                    val += x
                Vt.append(val)
            for j in range(len(rt)):
                Vt[j] += coeff[2] + C1 / exp(C2 * s_t)

        for i in range(len(rr)):
            Vr[i].append(t0(rr[i], coeff[0]))
        for i in range(len(rr)):
            for j in range(1, len(tr)):
                val = 0
                for k in range(1, len(C1k)):
                    val += j0(C1k[k] * rr[i]) * C2k[k] / exp((C3k[k] * tr[j]))
                Vr[i].append(val)
        for i in range(len(rr)):
            for j in range(1, len(tr)):
                Vr[i][j] += coeff[2] + C1 / exp(C2 * tr[j])
        print('VT', Vt)
        print(len(Vt))
        print('VR', Vr)
        print(len(Vr))
        plt1(window, Vt, rt, tt, Vr, rr, tr, s_i, s_k, schema_solve, tr_arr, rt_arr, K_arr, I_arr, K_factor, I_factor)
    else:
        schema_solve = scheme[coeff[13]](coeff)
        tr = [i * ht for i in range(K + 1)]
        rt = [i * hr for i in range(I + 1)]
        si_arr = [i * int(I / 10) for i in range(10)]
        sk_arr = [i * int(K / 10) for i in range(10)]
        si_arr.append(I)
        sk_arr.append(K)
        plt2(window, rt, tr, si_arr, sk_arr, schema_solve)


def plt0(window, Vt, rt, tt, Vr, rr, tr, s_i, s_k, schema_solve):

    fig = Figure(figsize=(10, 5), dpi=100)
    colors = ["red", "blue", "green", "black", "orange", "peru", "aqua", "pink", "olive", "lime"]
    plot1 = fig.add_subplot(1, 2, 1)
    plot2 = fig.add_subplot(1, 2, 2)
    max_e = 0
    #print("len Vt", len(Vt))
    #print("len Vt[0]", len(Vt[0]))
    #print('size', schema_solve.shape)
    #print('Vt', Vt)
    #print('Vr', Vr)
    for k in range(len(Vt)):
        for i in range(len(Vt[0])):
            temp = abs(Vt[k][i]-schema_solve[k, i])
            if temp > max_e:
                max_e = temp
    plot1.set_title(f'Погрешность = {max_e}')
    plot2.set_xlabel('t, с', fontsize=14)
    plot2.set_ylabel('V(r, t), град', fontsize=14)
    plot1.set_xlabel('r, см', fontsize=14)
    plot1.set_ylabel('V(r, t), град', fontsize=14)
    plot2.plot(tr, Vr[s_i], color=colors[0], label=f'r={round(rr[s_i], 2)}')
    plot1.plot(rt, Vt[s_k], color=colors[0], label=f't={round(tt[s_k], 2)}')
    plot2.plot(tr, schema_solve[:, s_i], color=colors[2], label=f'r={round(rr[s_i], 2)} (S)')
    plot1.plot(rt, schema_solve[s_k, :], color=colors[2], label=f't={round(tt[s_k], 2)} (S)')
    plot1.legend(fontsize="small")
    plot2.legend(fontsize="small")

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()

    canvas.get_tk_widget().pack()

    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()

    canvas.get_tk_widget().pack()


def plt1(window, Vt, rt, tt, Vr, rr, tr, s_i, s_k, schema_solve, tr_arr, rt_arr, K_arr, I_arr, K_factor, I_factor):
    fig = Figure(figsize=(10, 5), dpi=100)
    colors = ["red", "blue", "green", "black", "orange", "peru", "aqua", "pink", "olive", "lime"]
    plot1 = fig.add_subplot(1, 2, 1)
    plot2 = fig.add_subplot(1, 2, 2)
    plot2.set_xlabel('t, с', fontsize=14)
    plot2.set_ylabel('V(r, t), град', fontsize=14)
    plot1.set_xlabel('r, см', fontsize=14)
    plot1.set_ylabel('V(r, t), град', fontsize=14)
    plot2.plot(tr, Vr[0], color=colors[0], label=f'r={round(rr[0], 2)}')
    plot1.plot(rt, Vt, color=colors[0], label=f't={round(tt[0], 2)}')
    for i in range(len(tr_arr)):
        plot2.plot(tr_arr[i], schema_solve[i][:, s_i * (I_factor ** i)], color=colors[i + 1], label=f'K={K_arr[i]}, I={I_arr[i]}')
        plot1.plot(rt_arr[i], schema_solve[i][s_k * (K_factor ** i), :], color=colors[i + 1], label=f'K={K_arr[i]}, I={I_arr[i]}')
    plot1.legend(fontsize="small")
    plot2.legend(fontsize="small")

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()

    canvas.get_tk_widget().pack()

    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()

    canvas.get_tk_widget().pack()


def plt2(window, rt, tr, si_arr, sk_arr, schema_solve):

    fig = Figure(figsize=(10, 5), dpi=100)
    colors = ["red", "blue", "green", "black", "orange", "peru", "aqua", "pink", "olive", "lime", "purple"]
    plot1 = fig.add_subplot(1, 2, 1)
    plot2 = fig.add_subplot(1, 2, 2)
    max_e = 0

    plot2.set_xlabel('t, с', fontsize=14)
    plot2.set_ylabel('V(r, t), град', fontsize=14)
    plot1.set_xlabel('r, см', fontsize=14)
    plot1.set_ylabel('V(r, t), град', fontsize=14)
    for i in range(len(si_arr)):
        plot2.plot(tr, schema_solve[:, si_arr[i]], color=colors[i], label=f'i={si_arr[i]}')
        plot1.plot(rt, schema_solve[sk_arr[i], :], color=colors[i], label=f'k={sk_arr[i]}')
    plot1.legend(fontsize="small")
    plot2.legend(fontsize="small")

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()

    canvas.get_tk_widget().pack()

    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()

    canvas.get_tk_widget().pack()


def plt3(window, Vt, rt, tt, Vr, rr, tr, s_i, s_k, runge, no_runge):
    fig = Figure(figsize=(10, 5), dpi=100)
    colors = ["red", "blue", "green", "black", "orange", "peru", "aqua", "pink", "olive", "lime"]
    plot1 = fig.add_subplot(1, 2, 1)
    plot2 = fig.add_subplot(1, 2, 2)
    plot2.set_xlabel('t, с', fontsize=14)
    plot2.set_ylabel('V(r, t), град', fontsize=14)
    plot1.set_xlabel('r, см', fontsize=14)
    plot1.set_ylabel('V(r, t), град', fontsize=14)
    plot2.plot(tr, Vr[0], color=colors[0], label=f'r={round(rr[0], 2)}')
    plot1.plot(rt, Vt, color=colors[0], label=f't={round(tt[0], 2)}')
    plot2.plot(tr, runge[:, s_i], color=colors[1], label=f'С Рунге')
    plot1.plot(rt, runge[s_k, :], color=colors[1], label=f'С Рунге')
    plot2.plot(tr, no_runge[:, s_i], color=colors[2], label=f'Без Рунге')
    plot1.plot(rt, no_runge[s_k, :], color=colors[2], label=f'Без Рунге')
    plot1.legend(fontsize="small")
    plot2.legend(fontsize="small")

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()

    canvas.get_tk_widget().pack()

    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()

    canvas.get_tk_widget().pack()


def plt4(window, Vt, rt, tt, Vr, rr, tr, s_i, s_k, schema_solve_ya, schema_solve_r, tr_arr, rt_arr, K_arr, I_arr, K_factor, I_factor):
    fig = Figure(figsize=(10, 5), dpi=100)
    colors = ["red", "blue", "green", "black", "orange", "peru", "aqua", "pink", "olive", "lime"]
    plot1 = fig.add_subplot(1, 2, 1)
    plot2 = fig.add_subplot(1, 2, 2)
    plot2.set_xlabel('t, с', fontsize=14)
    plot2.set_ylabel('V(r, t), град', fontsize=14)
    plot1.set_xlabel('r, см', fontsize=14)
    plot1.set_ylabel('V(r, t), град', fontsize=14)
    plot2.plot(tr, Vr[0], color=colors[0], label=f'r={round(rr[0], 2)}')
    plot1.plot(rt, Vt, color=colors[0], label=f't={round(tt[0], 2)}')
    for i in range(len(tr_arr)):
        plot2.plot(tr_arr[i], schema_solve_ya[i][:, s_i * (I_factor ** i)], color=colors[i + 1], label=f'K={K_arr[i]}, I={I_arr[i]} Я')
        plot1.plot(rt_arr[i], schema_solve_ya[i][s_k * (K_factor ** i), :], color=colors[i + 1], label=f'K={K_arr[i]}, I={I_arr[i]} Я')
        plot2.plot(tr_arr[i], schema_solve_r[i][:, s_i * (I_factor ** i)], color=colors[i + 5], label=f'K={K_arr[i]}, I={I_arr[i]} Р')
        plot1.plot(rt_arr[i], schema_solve_r[i][s_k * (K_factor ** i), :], color=colors[i + 5], label=f'K={K_arr[i]}, I={I_arr[i]} Р')
    plot1.legend(fontsize="small")
    plot2.legend(fontsize="small")

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()

    canvas.get_tk_widget().pack()

    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()

    canvas.get_tk_widget().pack()