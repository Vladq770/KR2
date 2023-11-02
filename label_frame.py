from tkinter import *


def validate_entry(symbol):
    return True


class LabelFr:
    def __init__(self, name, fr, col, row, font, val):
        label_frame = LabelFrame(fr)
        self.entry = Entry(label_frame, validate="key", validatecommand=(fr.register(validate_entry), "%S"))
        self.entry.grid(column=1, row=0, padx=5)
        self.entry.insert(0, val)
        self.label = Label(label_frame, text=name, width=15, font=font)
        self.label.grid(column=0, row=0)
        label_frame.grid(column=col, row=row, pady=5, padx=10)

    def get(self):
        return self.entry.get()
