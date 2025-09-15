import tkinter as tk
import sys
import traceback

class RedirectText:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)  # Scroll to the end

    def flush(self):
        pass  # No need to implement flush for this example

def create_window():
    root = tk.Tk()
    root.title("Output Window")

    # Create a Text widget to display output
    text_widget = tk.Text(root, wrap='word', height=20, width=80)
    text_widget.pack(expand=True, fill='both')

    # Redirect stdout and stderr
    sys.stdout = RedirectText(text_widget)
    sys.stderr = RedirectText(text_widget)

    # Example function to generate output
    def generate_output():
        print("This is a standard output message.")
        try:
            # Intentionally raise an exception to demonstrate error handling
            raise Exception("This is an error message.")
        except Exception as e:
            # Capture and print the traceback
            traceback.print_exc()
            
    # Button to trigger output generation
    button = tk.Button(root, text="Generate Output", command=generate_output)
    button.pack()

    root.mainloop()

if __name__ == "__main__":
    create_window()