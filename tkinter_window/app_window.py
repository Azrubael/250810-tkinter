import tkinter as tk
from tkinter import filedialog, messagebox


class AppWindow(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Tkinter File Reader")
        self.geometry("500x200")
        self._create_menu()
        self._create_canvas()


    def _create_menu(self):
        menubar = tk.Menu(self)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(label="Open ШПС", command=self.open_shps)
        file_menu.add_command(label="Open ВОП", command=self.open_vop)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=False)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menubar)


    def _create_canvas(self):
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        # initial text
        self.text_shpk = self.canvas.create_text(
            10, 10,
            anchor="nw",
            text="No shpk file selected.",
            font=("Arial", 10),
            fill="black"
        )
        self.text_vop = self.canvas.create_text(
            10, 24,
            anchor="nw",
            text="No vop file selected.",
            font=("Arial", 10),
            fill="black"
        )


    def open_shps(self):
        filename = filedialog.askopenfilename(title="Select a file")
        if filename:
            # Update canvas text with file name
            self.canvas.itemconfigure(self.text_shpk, text=filename)


    def open_vop(self):
        filename = filedialog.askopenfilename(title="Select a file")
        if filename:
            # Update canvas text with file name
            self.canvas.itemconfigure(self.text_vop, text=filename)


    def show_about(self):
        messagebox.showinfo("About", "Simple Tkinter app — selects a file and shows its path on the canvas.")