import tkinter as tk
import math

current_angle = 0

def draw_epicycloid(canvas, R, r, d, angle_offset):
    global current_angle
    canvas.delete("angle_text")
    canvas.create_text(300, 20, text=f"Current Angle: {current_angle:.2f}°", font=("Arial", 12), fill="black", tags="angle_text")
    num_points = 10 * R
    points = []
    for i in range(num_points):
        theta = i * (2 * math.pi / num_points) + current_angle + angle_offset
        x = (R + r) * math.cos(theta) - d * math.cos((R + r) / r * theta)
        y = (R + r) * math.sin(theta) - d * math.sin((R + r) / r * theta)
        points.append((x + 300, y + 300))  # Centering shift

    for i in range(len(points) - 1):
        canvas.create_line(points[i], points[i + 1], fill="blue")


def on_button_click():
    global current_angle
    draw_epicycloid(canvas, R, r, d, math.radians(current_angle))
    current_angle += 360 - R / r


def on_clear_button_click():
    global current_angle
    current_angle = 0
    canvas.delete("all")


# create a new window
root = tk.Tk()
root.title("Epicycloid")

# Create a new canvas
canvas = tk.Canvas(root, width=600, height=600, bg="white")
canvas.pack()

# Parameters for the epycycle
R = 210  # Static circle radius
r = 25   # Rotating circle radius
d = 45   # Point radius to draw the epicycle
draw_epicycloid(canvas, R, r, d, math.radians(current_angle))

# Drawing the epicycloid
draw_button = tk.Button(root, text="Continue", command=on_button_click)
draw_button.pack(side=tk.RIGHT)

clear_button = tk.Button(root, text="Clear", command=on_clear_button_click)
clear_button.pack(side=tk.RIGHT, padx=(0, 25))

# Run
root.mainloop()
