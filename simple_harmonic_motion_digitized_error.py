# Simple harmonic motion (Digitized error)

import numpy as np
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.patches as patches
import tkinter as tk


def change_range_x(value):
    global x_min, x_max
    x_max = float(value)
    x_min = -amplitude * 1.4
    ax.set_xlim(x_min, x_max)
    tx_step.set_position([x_min, y_max * 0.95])


def change_range_y(value):
    global tx_step, y_min, y_max
    y_min = - float(value)
    y_max = float(value)
    ax.set_ylim(y_min, y_max)
    tx_step.set_position([x_min, y_max * 0.95])


def change_amp(value):
    global amplitude, y_ball1, y_dot0, circle, radius_ball, radius_dot
    amplitude = float(value)
    print(amplitude)
    y_ball1 = amplitude
    y_dot0 = amplitude
    update_ball()
    circle.radius = amplitude
    radius_ball = amplitude * 0.05
    radius_dot = radius_ball
    ball1.radius = radius_ball
    dot0.radius = radius_dot


def change_k(value):
    global k, omega
    k = float(value)
    omega = np.sqrt(k / mass)


def change_mass(value):
    global mass, omega
    mass = float(value)
    omega = np.sqrt(k / mass)


def clear_position():
    global is_play, cnt, tx_step, y_ball1, v_ball1, x_dot0, y_dot0
    is_play = False
    cnt = 0
    tx_step.set_text("Step=" + str(cnt))
    y_ball1 = amplitude
    v_ball1 = 0.
    x_dot0 = 0.
    y_dot0 = amplitude
    update_ball()


def update_ball():
    global y_ball1, ball1, x_dot0, y_dot0, line_ball1, line_dot0
    ball1.set_center([x_ball1, y_ball1])
    dot0.set_center([x_dot0, y_dot0])
    line_ball1.set_data([x_ball1, x_ball1], [0., y_ball1])
    line_dot0.set_data([0., x_dot0], [y_dot0, y_dot0])


def next_generation_ball1():
    global y_ball1, v_ball1
    force = - k * y_ball1
    a = force / mass
    v_ball1 = v_ball1 + a
    y_ball1 = y_ball1 + v_ball1


def next_generation_dot0():
    global y_dot0, x_dot0
    y_dot0 = amplitude * np.cos(omega * cnt)
    x_dot0 = - amplitude * np.sin(omega * cnt)


def on_change_window(e):
    if not is_play:
        update_ball()


def switch():
    global is_play
    if is_play:
        is_play = False
    else:
        is_play = True


def update(f):
    global tx_step, cnt, curve0, y_curve0, y_curve1
    if is_play:
        tx_step.set_text("Step=" + str(cnt))
        cnt += 1
        next_generation_dot0()
        next_generation_ball1()
        update_ball()
        y_curve0_roll = np.roll(y_curve0, 1)
        y_curve0 = y_curve0_roll
        y_curve0[0] = y_dot0
        curve0.set_ydata(y_curve0)
        y_curve1_roll = np.roll(y_curve1, 1)
        y_curve1 = y_curve1_roll
        y_curve1[1] = y_ball1
        curve1.set_ydata(y_curve1)


# Global variables
# Coordination
range_x_init = 10.
range_y_init = 5.
x_min = -15.
x_max = range_x_init
y_min = - range_y_init
y_max = range_y_init

# Parameters
mass = 200.
mass_init = mass
k = 1.
k_init = k

omega = np.sqrt(k/mass)

amplitude = 4.
x_min = -amplitude * 1.4

x_dot0 = 0.
y_dot0 = amplitude

x_ball1 = 0.
y_ball1 = amplitude
v_ball1 = 0.

radius_ball = amplitude * 0.05
radius_dot = radius_ball

# Animation control
cnt = 0
is_play = False

# Generate figure and axes
fig = Figure()
ax = fig.add_subplot(111)
ax.set_title("Simple harmonic motion (Digitized error)")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_aspect("equal")
ax.grid()

# Generate items
# Counter
tx_step = ax.text(x_min, y_max * 0.95, "Step=" + str(0))

# Graphic items
circle = patches.Circle(xy=(0., 0.), radius=amplitude, color='orange', fill=False)
ax.add_patch(circle)
dot0 = patches.Circle(xy=(x_dot0, y_dot0), radius=radius_dot, color='orange')
ax.add_patch(dot0)

ball1 = patches.Circle(xy=(x_ball1, y_ball1), radius=radius_ball, color='blue')
ax.add_patch(ball1)

line_ball1, = ax.plot([x_ball1, x_ball1], [0., y_ball1], color='blue', linestyle='--')
line_dot0, = ax.plot([0, x_dot0], [y_dot0, y_dot0], linewidth=1, color='orange', linestyle='-.')

x_curve = np.linspace(0, x_max, 500)
y_curve0 = x_curve * 0.
curve0, = ax.plot(x_curve, y_curve0, linestyle='-', label="y=A*cos(omega*step)", color='orange')
y_curve1 = x_curve * 0.
curve1, = ax.plot(x_curve, y_curve1, linestyle='-', label="Simulation", color='blue')

ax.legend(prop={"size": 8}, loc="best")

# Tkinter
root = tk.Tk()
root.title("Simple harmonic motion (Digitized error)")
canvas = FigureCanvasTkAgg(fig, root)
canvas.get_tk_widget().pack(expand=True, fill='both')

toolbar = NavigationToolbar2Tk(canvas, root)
canvas.get_tk_widget().pack()

# Play and pause button
btn_pp = tk.Button(root, text="Play/Pause", command=switch)
btn_pp.pack(side='left')

# Clear button
btn_clr = tk.Button(root, text="Clear", command=clear_position)
btn_clr.pack(side='left')

# x, y
lbl_x = tk.Label(root, text="Range-x")
lbl_x.pack(side='left')
var_x = tk.StringVar(root)  # variable for spinbox-value
var_x.set(range_x_init)  # Initial value
spn_x = tk.Spinbox(
    root, textvariable=var_x, format="%.1f", from_=5., to=40., increment=5.,
    command=lambda: change_range_x(var_x.get()), width=4
    )
spn_x.pack(side='left')
lbl_y = tk.Label(root, text="Range-y")
lbl_y.pack(side='left')
var_y = tk.StringVar(root)  # variable for spinbox-value
var_y.set(range_y_init)  # Initial value
spn_y = tk.Spinbox(
    root, textvariable=var_y, format="%.1f", from_=1., to=20.0, increment=1.,
    command=lambda: change_range_y(var_y.get()), width=4
    )
spn_y.pack(side='left')

# k (spring constant)
label_k = tk.Label(root, text="k(Spring constant)")
label_k.pack(side='left')
var_k = tk.StringVar(root)  # variable for spinbox-value
var_k.set(k_init)  # Initial value
s_k = tk.Spinbox(
    root, textvariable=var_k, format="%.1f", from_=1., to=100., increment=1.,
    command=lambda: change_k(var_k.get()), width=4
    )
s_k.pack(side='left')

# Mass
label_m = tk.Label(root, text=", m(Mass)")
label_m.pack(side='left')
var_m = tk.StringVar(root)  # variable for spinbox-value
var_m.set(mass_init)  # Initial value
s_m = tk.Spinbox(
    root, textvariable=var_m, format="%.1f", from_=1., to=400., increment=1.,
    command=lambda: change_mass(var_m.get()), width=4
    )
s_m.pack(side='left')

# Amplitude
label_amp = tk.Label(root, text=", A(Amplitude)")
label_amp.pack(side='left')
var_amp = tk.StringVar(root)  # variable for spinbox-value
var_amp.set(amplitude)  # Initial value
s_amp = tk.Spinbox(
    root, textvariable=var_amp, format="%.1f", from_=0., to=10., increment=1.,
    command=lambda: change_amp(var_amp.get()), width=4
    )
s_amp.pack(side='left')

# Draw animation
anim = animation.FuncAnimation(fig, update, interval=100, save_count=100)
root.bind('<Configure>', on_change_window)
root.mainloop()
