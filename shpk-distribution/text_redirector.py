from queue import Queue, Empty
import tkinter as tk

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