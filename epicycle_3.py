import tkinter as tk
import math

current_angle = 0

def draw_epicycloid(canvas, R, r, d, angle_offset):
    global current_angle
    canvas.delete("angle_text")
    offset = angle_offset / 3.14
    canvas.create_text(15, 15, text=f"Offset: {offset:.2f}", font=("Arial", 10), fill="black", tags="angle_text", anchor="w")
    num_points = 10 * R
    points = []
    for i in range(num_points):
        theta = i * (2 * math.pi / num_points) + current_angle + angle_offset
        x = (R + r) * math.cos(theta) - d * math.cos((R + r) / r * theta)
        y = (R + r) * math.sin(theta) - d * math.sin((R + r) / r * theta)
        points.append((x + 300, y + 300))  # Centering shift

    for i in range(len(points) - 1):
        canvas.create_line(points[i], points[i + 1], fill="blue")

    current_angle += 180


def on_button_click():
    global current_angle
    draw_epicycloid(canvas, R, r, d, math.radians(current_angle))
    

def on_clear_button_click():
    global current_angle
    current_angle = 0
    canvas.delete("all")


# create a new window
root = tk.Tk()
root.title("Epicycloid")
window_width = 600
window_height = 600
x_offset = 20  # Set the desired x position
y_offset = 20  # Set the desired y position
root.geometry(f"{window_width}x{window_height+40}+{x_offset}+{y_offset}")

# Create a new canvas
canvas = tk.Canvas(root, width=window_width, height=window_height, bg="white")
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
