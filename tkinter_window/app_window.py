import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from queue import Queue, Empty
from text_redirector import TextRedirector


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


    def _create_top_canvas(self):
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.pack(fill=tk.X, expand=False, side="top")
        # initial text
        self.text_shpk = self.canvas.create_text(
            10, 10,
            anchor="nw",
            text="Файл ШПК не обраний.",
            font=("Arial", 10),
            fill="black"
        )
        self.text_vop = self.canvas.create_text(
            10, 24,
            anchor="nw",
            text="Файл ВОП не обраний.",
            font=("Arial", 10),
            fill="black"
        )


    def open_shps(self):
        filename = filedialog.askopenfilename(title="Select a file")
        message = f"Файл ШПК: {filename}"
        if filename:
            # Update canvas text with file name
            self.canvas.itemconfigure(self.text_shpk, text=message)


    def open_vop(self):
        filename = filedialog.askopenfilename(title="Select a file")
        message = f"Файл ВОП: {filename}"
        if filename:
            # Update canvas text with file name
            self.canvas.itemconfigure(self.text_vop, text=message)


    def show_about(self):
        messagebox.showinfo("About", "Simple Tkinter app — selects a file and shows its path on the canvas.")


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