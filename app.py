from tkinter import *
from tkinter import ttk
from label_frame import LabelFr
from func_buttons import enter


root = Tk(baseName="123")
root.title("УМФ")
font = ('Times 14')
frm = ttk.Frame(root, padding=10)
frm.grid(column=0, row=0)
frm_buttons = ttk.Frame(root, padding=10)
frm_buttons.grid(column=1, row=0, rowspan=2)
label_R = LabelFr("R", frm, 0, 0)
label_L = LabelFr("L", frm, 0, 1)
label_Uc = LabelFr("Uc", frm, 0, 2)
label_alpha = LabelFr("alpha", frm, 0, 3)
label_T = LabelFr("T", frm, 0, 4)
label_k = LabelFr("k", frm, 0, 5)
label_c = LabelFr("c", frm, 0, 6)
label_t_min = LabelFr("Tmin", frm, 0, 7)
label_e = LabelFr("e", frm, 0, 8)
Button(frm, text="Ввод", font=font, command=lambda : enter(labels_fr, root)).grid(column=0, row=9)

labels_fr = [label_R, label_L, label_Uc, label_alpha, label_T, label_k, label_c, label_t_min, label_e]

root.mainloop()
