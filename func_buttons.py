import tkinter
import tkinter.messagebox as mb

from chart import chart


def enter(frames: list, root):
    coefficients = []
    for i in range(len(frames)):
        try:
            x = float(frames[i].get())
            print(x, type(x))
        except ValueError:
            msg = f'Неверный ввод в строке {i + 1}'
            mb.showerror("Ошибка", msg)
            return
        coefficients.append(x)
    for i in range(len(coefficients)):
        if i in (0, 1, 3, 4, 5, 6, 7, 8) and coefficients[i] <= 0:
            msg = f'Неверный ввод в строке {i + 1} (необходимо положительное число)'
            mb.showerror("Ошибка", msg)
            return
        if i == 7:
            if coefficients[i] >= coefficients[4]:
                msg = f'Неверный ввод в строке {i + 1} (Tmin >= T)'
                mb.showerror("Ошибка", msg)
                return
            """if coefficients[i] < 0.01:
                msg = f'Неверный ввод в строке {i + 1} (Tmin не может быть меньше 0.01)'
                mb.showerror("Ошибка", msg)
                return"""
    newWindow = tkinter.Toplevel(root)
    newWindow.grab_set()
    chart(coefficients, newWindow)


