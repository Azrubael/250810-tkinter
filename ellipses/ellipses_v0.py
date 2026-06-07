import tkinter as tk
import math

def draw_elliptic_curve(canvas, a, b, scale=20, x_range=(-10, 10)):
    """
    Draws the elliptic curve y^2 = x^3 + a*x + b on the given canvas.
    """
    width = int(canvas['width'])
    height = int(canvas['height'])
    center_x = width // 2
    center_y = height // 2

    # Draw axes
    canvas.create_line(0, center_y, width, center_y, fill="gray")
    canvas.create_line(center_x, 0, center_x, height, fill="gray")

    # Plot points
    for x in [i * 0.1 for i in range(int(x_range[0]*10), int(x_range[1]*10))]:
        rhs = x**3 + a*x + b
        if rhs >= 0:  # Only real solutions
            y = math.sqrt(rhs)
            # Scale and translate
            px = center_x + x * scale
            py1 = center_y - y * scale
            py2 = center_y + y * scale
            canvas.create_oval(px-2, py1-2, px+2, py1+2, fill="blue")
            canvas.create_oval(px-2, py2-2, px+2, py2+2, fill="blue")

def main():
    root = tk.Tk()
    root.title("Elliptic Curve")

    canvas = tk.Canvas(root, width=800, height=600, bg="white")
    canvas.pack()

    # Hardcoded parameters for elliptic curve y^2 = x^3 + ax + b
    a = -1
    b = 1
    draw_elliptic_curve(canvas, a, b, scale=30, x_range=(-5, 5))

    root.mainloop()

if __name__ == "__main__":
    main()
