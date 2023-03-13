from calculations import calculation
from mpmath import j0
from math import e
import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
import matplotlib.pyplot as plt
import numpy as np

mpl.use('TkAgg')

def chart(coeff: list, window):
    C1, C2, C1k, C2k, C3k = calculation(coeff)
    print(C1)
    print(C2)
    print(C1k)
    print("C2k", C2k)
    print(C3k)
    rt = np.linspace(0, coeff[0], 200)
    tt = np.linspace(0, coeff[4], 5)
    Vt = [[], [], [], [], []]
    rr = np.linspace(0, coeff[0], 5)
    tr = np.linspace(0, coeff[4], 200)
    Vr = [[], [], [], [], []]
    for i in range(len(tt)):
        for j in range(len(rt)):
            val = 0
            for k in range(len(C1k)):
                x = j0(C1k[k] * rt[j]) * C2k[k] / e ** (C3k[k] * tt[i])
                val += x
                #print(j0(C1k[k] * rt[j]))
                #print(j0(C1k[k] * rt[j]) * C2k[k])
                #print(e ** (C3k[k] * tt[i]))
                #print(j0(C1k[k] * rt[j]) * C2k[k] / e ** (C3k[k] * tt[i]))
                #print(x, tt[i], rt[j])
            Vt[i].append(val)
    for i in range(len(tt)):
        for j in range(len(rt)):
            Vt[i][j] += coeff[2] + C1 / e ** (C2 * tt[i])

    for i in range(len(rr)):
        for j in range(len(tr)):
            val = 0
            for k in range(len(C1k)):
                val += j0(C1k[k] * rr[i]) * C2k[k] / e ** (C3k[k] * tr[j])
            Vr[i].append(val)
    for i in range(len(rr)):
        for j in range(len(tr)):
            Vt[i][j] += coeff[2] + C1 / e ** (C2 * tr[j])



    plot(window, Vt, rt, tt, Vr, rr, tr)


def plot(window, Vt, rt, tt, Vr, rr, tr):

    fig = Figure(figsize=(10, 5), dpi=100)

    plot1 = fig.add_subplot(1, 2, 1)
    plot2 = fig.add_subplot(1, 2, 2)
    plot2.set_xlabel('t', fontsize=14)
    plot2.set_ylabel('V(r, t)', fontsize=14)
    plot1.set_xlabel('r', fontsize=14)
    plot1.set_ylabel('V(r, t)', fontsize=14)
    plot1.plot(rt, Vt[0],  color='red',  label=f't={tt[0]}')
    plot1.plot(rt, Vt[1],  color='blue',  label=f't={tt[1]}')
    plot1.plot(rt, Vt[2],  color='green',  label=f't={tt[2]}')
    plot1.plot(rt, Vt[3],  color='black',  label=f't={tt[3]}')
    plot1.plot(rt, Vt[4],  color='orange',  label=f't={tt[4]}')
    plot1.legend()
    plot2.plot(tr, Vr[0], color='red', label=f'r={rr[0]}')
    plot2.plot(tr, Vr[1], color='blue', label=f'r={rr[1]}')
    plot2.plot(tr, Vr[2], color='green', label=f'r={rr[2]}')
    plot2.plot(tr, Vr[3], color='black', label=f'r={rr[3]}')
    plot2.plot(tr, Vr[4], color='orange', label=f'r={rr[4]}')
    plot2.legend()

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()

    canvas.get_tk_widget().pack()

    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()

    canvas.get_tk_widget().pack()