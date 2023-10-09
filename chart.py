from calculations import calculation, t0
from explicit_schema import solve_schema0
from implicit_schema import solve_schema1
from mpmath import *
import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
import matplotlib.pyplot as plt
import numpy as np

mpl.use('TkAgg')

def chart(coeff: list, window):
    schema_solve = None
    C1, C2, C1k, C2k, C3k = calculation(coeff)
    if coeff[13] == 1:
        schema_solve = solve_schema1(coeff)
    elif coeff[13] == 0:
        schema_solve = solve_schema0(coeff)
    print("Solve", schema_solve)
    K = int(coeff[9])
    I = int(coeff[10])
    s_k = int(coeff[11])
    s_i = int(coeff[12])
    hr = coeff[0] / I
    ht = coeff[4] / K
    s_t = int(coeff[11]) * ht
    s_r = int(coeff[12]) * hr
    tt = [s_k * ht]
    rr = [s_i * hr]
    print("rr", rr)
    print("tt", tt)
    tr = [i * ht for i in range(K + 1)]
    rt = [i * hr for i in range(I + 1)]
    print("rt", rt)
    print("tr", tr)
    Vt = []
    Vr = []
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

    for i in rr:
        Vr.append(t0(i, coeff[0]))
    for j in range(1, len(tr)):
        val = 0
        for k in range(1, len(C1k)):
            val += j0(C1k[k] * s_r) * C2k[k] / exp((C3k[k] * tr[j]))
        Vr.append(val)
    for j in range(1, len(tr)):
        Vr[j] += coeff[2] + C1 / exp(C2 * tr[j])

    plot(window, Vt, rt, tt, Vr, rr, tr, s_i, s_k, schema_solve)


def plot(window, Vt, rt, tt, Vr, rr, tr,s_i, s_k, schema_solve):

    fig = Figure(figsize=(10, 5), dpi=100)
    colors = ["red", "blue", "green", "black", "orange", "peru", "aqua", "pink", "olive", "lime"]
    plot1 = fig.add_subplot(1, 2, 1)
    plot2 = fig.add_subplot(1, 2, 2)
    max_t = max_r = 0
    for i in range(len(Vt)):
        temp = abs(Vt[i]-schema_solve[s_k,i])
        if temp > max_t:
            max_t = temp
    for i in range(len(Vr)):
        temp = abs(Vr[i]-schema_solve[i,s_i])
        if temp > max_r:
            max_r = temp
    plot1.set_title(f'Погрешность = {max_t}')
    plot2.set_title(f'Погрешность = {max_r}')
    plot2.set_xlabel('t, с', fontsize=14)
    plot2.set_ylabel('V(r, t), град', fontsize=14)
    plot1.set_xlabel('r, см', fontsize=14)
    plot1.set_ylabel('V(r, t), град', fontsize=14)
    plot2.plot(tr, Vr, color=colors[0], label=f'r={rr[0]}')
    plot1.plot(rt, Vt, color=colors[0], label=f't={tt[0]}')
    plot2.plot(tr, schema_solve[:,s_i], color=colors[2], label=f'r={rr[0]}')
    plot1.plot(rt, schema_solve[s_k,:], color=colors[2], label=f't={tt[0]}')
    plot1.legend(fontsize="small")
    plot2.legend(fontsize="small")

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()

    canvas.get_tk_widget().pack()

    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()

    canvas.get_tk_widget().pack()