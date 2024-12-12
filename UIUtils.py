import tkinter as tk

def create_label(parent, text, row, column, padx=5, pady=5):
    label = tk.Label(parent, text=text)
    label.grid(row=row, column=column, padx=padx, pady=pady)
    return label

def create_button(parent, text, command, row, column, padx=5, pady=5):
    button = tk.Button(parent, text=text, command=command)
    button.grid(row=row, column=column, padx=padx, pady=pady)
    return button
