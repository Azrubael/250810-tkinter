import tkinter as tk
import math

def draw_epicycloid(canvas, R, r, d, num_points=10000):
    points = []
    for i in range(num_points):
        theta = i * (2 * math.pi / num_points)
        x = (R + r) * math.cos(theta) - d * math.cos((R + r) / r * theta)
        y = (R + r) * math.sin(theta) - d * math.sin((R + r) / r * theta)
        points.append((x + 300, y + 300))  # Centering shift

    for i in range(len(points) - 1):
        canvas.create_line(points[i], points[i + 1], fill="blue")

# create a new window
root = tk.Tk()
root.title("Epicycloid")

# Create a new canvas
canvas = tk.Canvas(root, width=600, height=600, bg="white")
canvas.pack()

# Parameters for the epycycle
R = 100  # Staric circle radius
r = 30   # Prbiting circle radius
d = 30   # Point radius to draw the epicycle

# Drawing the epicycloid
draw_epicycloid(canvas, R, r, d)

# Run
root.mainloop()
