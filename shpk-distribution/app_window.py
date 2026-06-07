import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from text_redirector import TextRedirector
from handle_xlsx import read_shpk_file, calculate_shpk_list, \
    save_report_ppd, update_distribution_report, save_report_vacation1

class AppWindow(tk.Tk):
    """
    Creates a Tk window containing a scrollable text canvas that captures stdout and stderr.
    """

    def __init__(self, title="Tkinter File Reader", width=640, height=480):
        super().__init__()
        self.title(title)
        self.geometry(f"{width}x{height}")
        self._create_menu()
        self._create_top_canvas()
        self.input_file = None          # Файл ШПК
        self.distribution_file = None   # Файл розподілу персонала
        self.output_file = None         # Файл звіту для ППД
        self.shpk_total_data = {}       # Зчитані дані ШПК у вигляді словника
        self.total_counter = {}         # Сумарні дані по кількості людей по категоріям
        self.divisions_counter = {}     # Кількісні дані розподілу персонала по категоріям і підрозділам
        self.report_counter = {}        # Структура кількісних даних у вигляді словника для звіту ППД
        self.personnel_distribution = {} # Список людей для звіту ППД

        # Main frame
        self.frame = tk.Frame(self)
        self.frame.pack(fill=tk.X, expand=True)

        # ScrolledText acts as the canvas for stdout/stderr
        self.output = ScrolledText(self.frame, wrap=tk.WORD, state='disabled')
        self.output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Add a simple toolbar with clear and close buttons
        toolbar = tk.Frame(self)
        toolbar.pack(fill=tk.X, side=tk.BOTTOM)
        clear_btn = tk.Button(toolbar, text="Clear", command=self.clear)
        clear_btn.pack(side=tk.LEFT, padx=4, pady=4)
        close_btn = tk.Button(toolbar, text="Close", command=self.close)
        close_btn.pack(side=tk.LEFT, padx=4, pady=4)

        # Optional styling for stderr vs stdout
        self.output.tag_configure("stderr", foreground="red")
        self.output.tag_configure("stdout", foreground="black")

        # Create redirectors
        self.stdout_redirector = TextRedirector(self.output, tag="stdout")
        self.stderr_redirector = TextRedirector(self.output, tag="stderr")

        # Save original streams so they can be restored if needed
        self._orig_stdout = sys.stdout
        self._orig_stderr = sys.stderr

        # Replace system stdout/stderr
        sys.stdout = self.stdout_redirector
        sys.stderr = self.stderr_redirector

        # Handle window close properly
        self.protocol("WM_DELETE_WINDOW", self.close)
        

    def _create_menu(self):
        menubar = tk.Menu(self)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(label="Вхідний файл ШПС", command=self.select_shps)
        file_menu.add_command(label="Вхідний файл розподілу", command=self.select_distribution)
        file_menu.add_command(label="Вихідний файл звіту", command=self.select_output)
        file_menu.add_separator()
        file_menu.add_command(label="Вихід", command=self.quit)
        menubar.add_cascade(label="Файл", menu=file_menu)
        
        # Utility menu
        utility_menu = tk.Menu(menubar, tearoff=False)
        utility_menu.add_command(label="Генерувати дані", command=self.generate_output)
        utility_menu.add_command(label="Записати звіт для стройової", \
                            command=self.report_ppd)
        utility_menu.add_command(label="Звіт по І частині щорічних відпусток", \
                            command=self.report_vacation1)
        utility_menu.add_command(label="Оновити файл розподілу", \
                            command=self.report_combat)

        utility_menu.add_command(label="Очистка вікна", command=self.clear)
        menubar.add_cascade(label="Використання", menu=utility_menu)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=False)
        help_menu.add_command(label="Прочитай мене", command=self.show_about)
        menubar.add_cascade(label="Допомога", menu=help_menu)

        self.config(menu=menubar)


    def _create_top_canvas(self):
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill=tk.X, expand=False, side="top")
        # initial text
        self.text_shpk = self.canvas.create_text(
            10, 10,
            anchor="nw",
            text="Вхідний файл ШПК не обраний.",
            font=("Arial", 10),
            fill="black"
        )
        self.text_distribution = self.canvas.create_text(
            10, 24,
            anchor="nw",
            text="Вхідний файл розподілу не обраний.",
            font=("Arial", 10),
            fill="black"
        )
        self.text_vop = self.canvas.create_text(
            10, 38,
            anchor="nw",
            text="Вихідний файл для звіту ППД не обраний.",
            font=("Arial", 10),
            fill="black"
        )


    def select_shps(self):
        """Вибір файлу ШПК та підготовка структури даних для аналізу
        """
        filename = filedialog.askopenfilename(title="Select a file")
        message = f"Файл ШПК: {filename}"
        if filename:
            # Update canvas text with file name
            self.canvas.itemconfigure(self.text_shpk, text=message)
        self.input_file = filename
        return filename


    def select_distribution(self):
        """Вибір файлу останнього розподілу людей для підготовки оновленого звіту
        """
        filename = filedialog.askopenfilename(title="Select a file")
        message = f"Файл розподілу: {filename}"
        if filename:
            # Update canvas text with file name
            self.canvas.itemconfigure(self.text_distribution, text=message)
        self.distribution_file = filename
        return filename


    def select_output(self):
        filename = filedialog.askopenfilename(title="Select a file")
        message = f"Файл звіту: {filename}"
        if filename:
            # Update canvas text with file name
            self.canvas.itemconfigure(self.text_vop, text=message)
        self.output_file = filename
        return filename


    def generate_output(self):
        """Генерація структур даних для формування звітів.
        Сгенеровані структури даних зберігаються в атрибутах класу AppWindow
        """
        import traceback
        try:
            if not self.input_file:
                raise Exception("Вхідний файл ШПК не обраний.")
            print("Дані генеруються...")
            self.shpk_total_data = read_shpk_file(self.input_file)
            self.total_counter, self.report_counter, \
                self.personnel_distribution = calculate_shpk_list(self.shpk_total_data)
            if self.shpk_total_data:
                print("Дані успішно підготовлено.")
                print(self.total_counter)
            else:
                raise Exception("Вхідні дані не підготовлено належним чином.")
        except Exception as e:
            # Capture and print the traceback
            traceback.print_exc()
            # self.canvas.itemconfigure(self.text_vop, text=message)


    def report_ppd(self):
        """Збереження звіту ППД.
        """
        if not self.input_file:
            raise Exception("Вхідний файл ШПК не обраний.")
        if not self.total_counter:
            raise Exception("Вхідні дані не сгенеровані.")
        if not self.output_file:
            print(f"Вихідний файл не обраний, використовую ім'я за замовчуванням.")
            save_report_ppd(self.total_counter, self.report_counter, \
                        self.personnel_distribution)
        elif os.path.exists(self.output_file):
            print(f"Зміст вихідного файлу {self.output_file} буде замінено.")
            save_report_ppd(self.total_counter, self.report_counter, \
                self.personnel_distribution, self.output_file)
        
        return


    def report_combat(self):
        """Збереження оновленого розподілу людей.
        """
        if not self.input_file:
            raise Exception("Вхідний файл ШПК не обраний.")
        if not self.shpk_total_data:
            raise Exception("Вхідні дані не зчитані.")
        if not self.distribution_file:
            raise Exception("Файл розподілу людей не обраний.")
        if not os.path.exists(self.distribution_file):
            raise Exception("Файл розподілу людей не існує.")
        if not self.output_file:
            print(f"Вихідний файл не обраний, використовую ім'я за замовчуванням.")
            update_distribution_report(self.shpk_total_data, \
                                       self.distribution_file)
        elif os.path.exists(self.output_file):
            print(f"Зміст вихідного файлу {self.output_file} буде оновлено.")
            update_distribution_report(self.shpk_total_data, \
                self.distribution_file, self.output_file)
        
        return
    

    def report_vacation1(self):
        if not self.input_file:
            raise Exception("Вхідний файл ШПК не обраний.")
        if not self.shpk_total_data:
            raise Exception("Вхідні дані не зчитані.")
        if not self.output_file:
            print(f"Вихідний файл не обраний, використовую ім'я за замовчуванням.")
            save_report_vacation1(self.shpk_total_data)
        else:
            print(f"Вихідний файл: {self.output_file}.")
            save_report_vacation1(self.shpk_total_data, self.output_file)
        
        return
    

    def show_about(self):
        messagebox.showinfo("Підказка", """Ця маленька програма призначена прискорити
підготовку трьох типів звітів.
\tПісля запуску цієї програми, з'явиться вікно,
де порібно обрати вхідний файл `xlsx` розподілу
особового складу.
\tПотрібно переконатись, що обрано саме
правильний файл ШПС, бо існує лише вбудована
перевірка назви аркуша `ШПС`.
\tПри обранні прототипу для звіту розподілу
особового складу, потрібно переконатись, що цей
файл може бути прототипом, бо існує лише
перевірка назви аркуша `3БО`.
\tДля генерації звіту по відпусткам потрібно
обрати вхідний файл `xlsx` розподілу особового
складу, а потім обрати команду `Генерувати дані`.""")


    def clear(self):
        """Clear the output widget."""
        self.output.configure(state='normal')
        self.output.delete('1.0', tk.END)
        self.output.configure(state='disabled')


    def close(self):
        """Restore stdout/stderr and destroy the window."""
        sys.stdout = self._orig_stdout
        sys.stderr = self._orig_stderr
        try:
            self.destroy()
        except tk.TclError:
            pass