import tkinter
import tkinter.messagebox as mb

from chart import chart


scheme = {'Явная схема': 0, 'Неявная схема': 1, 'Схема Кранка-Николсона': 2, 'Явная(Рунге)': 3, 'Явная+Рунге': 4}
type_chart = {'Погрешность': 0, 'Изменение K, I': 1, 'На разных слоях': 2}
def enter(frames: list, root):
    coefficients = []
    for i in range(len(frames) - 2):
        try:
            x = float(frames[i].get())
            print(x, type(x))
        except ValueError:
            msg = f'Неверный ввод в строке {i + 1}'
            mb.showerror("Ошибка", msg)
            return
        coefficients.append(x)
    coefficients.append(scheme[frames[13].get()])
    coefficients.append(type_chart[frames[14].get()])
    print('TYPE CHART', coefficients[14])
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


