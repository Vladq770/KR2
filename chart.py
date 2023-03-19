from calculations import calculation, t0
from mpmath import *
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
    tt = []
    rr = []
    rt = np.linspace(0, coeff[0], 200)
    t1 = np.linspace(0, coeff[4] * 0.25, 5)
    t2 = np.linspace(coeff[4] * 0.25, coeff[4], 6)
    r1 = np.linspace(0, coeff[0] * 0.25, 5)
    r2 = np.linspace(coeff[0] * 0.25, coeff[0], 6)
    for i in range(5):
        tt.append(t1[i])
    for i in range(1, 6):
        tt.append(t2[i])
    for i in range(5):
        rr.append(r1[i])
    for i in range(1, 6):
        rr.append(r2[i])
    print("Version", mpl.__version__)
    print("rr", rr)
    print("tt", tt)
    Vt = [[], [], [], [], [], [], [], [], [], []]
    tr = np.linspace(0, coeff[4], 200)
    Vr = [[], [], [], [], [], [], [], [], [], []]
    for i in range(len(rt)):
        Vt[0].append(t0(rt[i], coeff[0]))
    for i in range(1, len(tt)):
        for j in range(len(rt)):
            val = 0
            for k in range(1, len(C1k)):
                x = j0(C1k[k] * rt[j]) * C2k[k] / exp((C3k[k] * tt[i]))
                val += x
                #print(j0(C1k[k] * rt[j]))
                #print(j0(C1k[k] * rt[j]) * C2k[k])
                #print(e ** (C3k[k] * tt[i]))
                #print(j0(C1k[k] * rt[j]) * C2k[k] / e ** (C3k[k] * tt[i]))
                #print(x, tt[i], rt[j])
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



    plot(window, Vt, rt, tt, Vr, rr, tr)


def plot(window, Vt, rt, tt, Vr, rr, tr):

    fig = Figure(figsize=(10, 5), dpi=100)
    colors = ["red", "blue", "green", "black", "orange", "peru", "aqua", "pink", "olive", "lime"]
    plot1 = fig.add_subplot(1, 2, 1)
    plot2 = fig.add_subplot(1, 2, 2)
    plot2.set_xlabel('t, с', fontsize=14)
    plot2.set_ylabel('V(r, t), град', fontsize=14)
    plot1.set_xlabel('r, см', fontsize=14)
    plot1.set_ylabel('V(r, t), град', fontsize=14)
    for i in range(10):
        plot1.plot(rt, Vt[i], color=colors[i], label=f't={tt[i]}')
        plot2.plot(tr, Vr[i], color=colors[i], label=f'r={rr[i]}')
    plot1.legend(fontsize="small")
    plot2.legend(fontsize="small")

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()

    canvas.get_tk_widget().pack()

    toolbar = NavigationToolbar2Tk(canvas, window)
    toolbar.update()

    canvas.get_tk_widget().pack()