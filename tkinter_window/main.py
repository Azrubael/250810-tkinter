#!/usr/bin/env python3
"""
Simple Tkinter app:
- Menu bar with File and Help menus
- File -> Open shows a file dialog; selected filename is printed on the Canvas
- Help -> About shows a simple info dialog
"""

from app_window import AppWindow



if __name__ == "__main__":
    app = AppWindow()
    app.mainloop()
