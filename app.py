from tkinter import *
from tkinter import ttk
from label_frame import LabelFr
from func_buttons import enter


root = Tk(baseName="123")
root.title("ЧММФ")
font = ('Times 14')
frm = ttk.Frame(root, padding=10)
frm.grid(column=0, row=0)
frm_buttons = ttk.Frame(root, padding=10)
frm_buttons.grid(column=1, row=0, rowspan=2)
label_R = LabelFr("R", frm, 0, 0, font)
label_L = LabelFr("L", frm, 0, 1, font)
label_Uc = LabelFr("Uc", frm, 0, 2, font)
label_alpha = LabelFr("alpha", frm, 0, 3, font)
label_T = LabelFr("T", frm, 0, 4, font)
label_k = LabelFr("k", frm, 0, 5, font)
label_c = LabelFr("c", frm, 0, 6, font)
label_t_min = LabelFr("Tmin", frm, 0, 7, font)
label_e = LabelFr("e", frm, 0, 8, font)
label_K = LabelFr("K", frm, 0, 9, font)
label_I = LabelFr("I", frm, 0, 10, font)
label_hrk = LabelFr("Слой k", frm, 0, 11, font)
label_hti = LabelFr("Слой i", frm, 0, 12, font)
Button(frm, text="Ввод", font=font, command=lambda : enter(labels_fr, root)).grid(column=0, row=15)
label_frame = LabelFrame(frm)
label = Label(label_frame, text="Тип схемы", width=15, font=('Times 14'))
label.grid(column=0, row=0)
label_frame.grid(column=0, row=13, pady=5, padx=10)
label_frame_chart = LabelFrame(frm)
label_chart = Label(label_frame_chart, text="Тип графика", width=15, font=('Times 14'))
label_chart.grid(column=0, row=0)
label_frame_chart.grid(column=0, row=14, pady=5, padx=10)
scheme = ('Явная схема', 'Неявная схема', 'Схема Кранка-Николсона', 'Явная(Рунге)')
var = StringVar(value=scheme[1])
combobox = ttk.Combobox(label_frame, textvariable=var)
combobox['values'] = scheme
combobox['state'] = 'readonly'
combobox.grid(column=1, row=0, padx=5)
type_chart = ('Погрешность', 'Изменение K, I', 'На разных слоях')
var_chart = StringVar(value=type_chart[0])
combobox_chart = ttk.Combobox(label_frame_chart, textvariable=var_chart)
combobox_chart['values'] = type_chart
combobox_chart['state'] = 'readonly'
combobox_chart.grid(column=1, row=0, padx=5)

labels_fr = [label_R, label_L, label_Uc, label_alpha, label_T, label_k, label_c, label_t_min, label_e, label_K, label_I,
             label_hrk, label_hti, combobox, combobox_chart]

root.mainloop()
