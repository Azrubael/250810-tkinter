import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from queue import Queue, Empty
import time

class TextRedirector:
    """
    Redirector that safely writes text into a tkinter Text widget from any thread.
    It uses a queue and schedules periodic polling on the Tk mainloop to flush items.
    """
    def __init__(self, text_widget, tag=None):
        self.text_widget = text_widget
        self.queue = Queue()
        self.tag = tag

        # Start the periodic flush loop on the widget's event loop
        self._schedule_flush()

    def write(self, msg):
        if not msg:
            return
        # Normalize to str
        self.queue.put(str(msg))

    def flush(self):
        # No-op for compatibility
        pass

    def _schedule_flush(self):
        try:
            self._flush_from_queue()
        finally:
            # schedule next flush
            self.text_widget.after(100, self._schedule_flush)

    def _flush_from_queue(self):
        try:
            while True:
                item = self.queue.get_nowait()
                # Insert at end and scroll to end
                self.text_widget.configure(state='normal')
                if self.tag:
                    self.text_widget.insert(tk.END, item, (self.tag,))
                else:
                    self.text_widget.insert(tk.END, item)
                self.text_widget.see(tk.END)
                self.text_widget.configure(state='disabled')
        except Empty:
            return


class AppWindow(tk.Tk):
    """
    Creates a Tk window containing a scrollable text canvas that captures stdout and stderr.
    """

    def __init__(self, title="Tkinter File Reader", width=640, height=480):
        super().__init__()
        self.title(title)
        self.geometry(f"{width}x{height}")
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