import tkinter as tk
from tkinter import messagebox

def on_button1_click():
    messagebox.showinfo("Info", "Ви натиснули кнопку 1!")

def on_button2_click():
    messagebox.showinfo("Info", "Ви натиснули кнопку 2!")

# Створення основного вікна
root = tk.Tk()
root.title("Вікно з кнопками")

# Створення кнопок
button1 = tk.Button(root, text="Кнопка 1", command=on_button1_click)
button1.pack(pady=10)

button2 = tk.Button(root, text="Кнопка 2", command=on_button2_click)
button2.pack(pady=10)

# Запуск основного циклу
root.mainloop()