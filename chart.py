from calculations import calculation, t0
from explicit_schema import solve_schema0
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
scheme = [solve_schema0, solve_schema1, solve_schema2]
def chart(coeff: list, window):
    C1, C2, C1k, C2k, C3k = calculation(coeff)
    schema_solve = scheme[coeff[13]](coeff)
    print("Solve", schema_solve)
    K = int(coeff[9])
    I = int(coeff[10])
    s_k = int(coeff[11])
    s_i = int(coeff[12])
    hr = coeff[0] / I
    ht = coeff[4] / K
    s_t = int(coeff[11]) * ht
    s_r = int(coeff[12]) * hr
    tr = [i * ht for i in range(K + 1)]
    rt = [i * hr for i in range(I + 1)]
    tt = tr
    rr = rt
    print("Version", mpl.__version__)
    print("rr", rr)
    print("tt", tt)
    print("rt", rt)
    print("tr", tr)
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

    plot(window, Vt, rt, tt, Vr, rr, tr, s_i, s_k, schema_solve)


def plot(window, Vt, rt, tt, Vr, rr, tr, s_i, s_k, schema_solve):

    fig = Figure(figsize=(10, 5), dpi=100)
    colors = ["red", "blue", "green", "black", "orange", "peru", "aqua", "pink", "olive", "lime"]
    plot1 = fig.add_subplot(1, 2, 1)
    plot2 = fig.add_subplot(1, 2, 2)
    max_e = 0
    print("len Vt", len(Vt))
    print("len Vt[0]", len(Vt[0]))
    print('size', schema_solve.shape)
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
    plot2.plot(tr, Vr[s_i], color=colors[0], label=f'r={rr[s_i]}')
    plot1.plot(rt, Vt[s_k], color=colors[0], label=f't={tt[s_k]}')
    plot2.plot(tr, schema_solve[:, s_i], color=colors[2], label=f'r={rr[s_i]} (S)')
    plot1.plot(rt, schema_solve[s_k, :], color=colors[2], label=f't={tt[s_k]} (S)')
    plot1.legend(fontsize="small")
    plot2.legend(fontsize="small")

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()

    canvas.get_tk_widget().pack()

    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()

    canvas.get_tk_widget().pack()