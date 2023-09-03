# Simple harmonic motion (Digitized error)

import numpy as np
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.patches as patches
import tkinter as tk


def change_amp(value):
    global amplitude, y_ball0, y_ball1, y_ball2, y_dot0, circle
    amplitude = float(value)
    print(amplitude)
    y_ball0 = amplitude
    y_ball1 = amplitude
    y_ball2 = amplitude
    y_dot0 = y_ball0
    update_ball()
    circle.radius = y_ball0


def change_k(value):
    global k, omega
    k = float(value)
    omega = np.sqrt(k / mass)


def change_mass(value):
    global mass, omega
    mass = float(value)
    omega = np.sqrt(k / mass)


def clear_position():
    global is_play, cnt, tx_step, y_ball0, y_ball1, y_ball2, v_ball1, v_ball2, cnt2, x_dot0, y_dot0
    is_play = False
    cnt = 0
    cnt2 = 0
    tx_step.set_text("Step=" + str(cnt2))
    y_ball0 = amplitude
    y_ball1 = amplitude
    y_ball2 = amplitude
    v_ball1 = 0.
    v_ball2 = 0.
    x_dot0 = 0.
    y_dot0 = y_ball0
    update_ball()


def update_ball():
    global y_ball0, y_ball1, y_ball2, ball0, ball1, ball2, x_dot0, y_dot0, line1, line2
    ball0.set_center([x_ball0, y_ball0])
    ball1.set_center([x_ball1, y_ball1])
    ball2.set_center([x_ball2, y_ball2])
    dot0.set_center([x_dot0, y_dot0])
    line1.set_data([x_ball1, x_ball1], [0., y_ball1])
    line2.set_data([x_ball2, x_ball2], [0., y_ball2])


def next_generation_ball2():
    global y_ball2, v_ball2, flag_ball2
    if flag_ball2:
        force = - k * y_ball2
        a = force / mass
        v_ball2 = v_ball2 + a
        flag_ball2 = False
    else:
        y_ball2 = y_ball2 + v_ball2
        flag_ball2 = True


def next_generation_ball1():
    global y_ball1, v_ball1
    force = - k * y_ball1
    a = force / mass
    v_ball1 = v_ball1 + a
    y_ball1 = y_ball1 + v_ball1


def next_generation_ball0():
    global y_ball0
    y_ball0 = amplitude * np.cos(omega * cnt2)


def next_generation_dot0():
    global y_dot0, x_dot0
    y_dot0 = amplitude * np.cos(omega * cnt2)
    x_dot0 = - amplitude * np.sin(omega * cnt2)


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
    global tx_step, cnt, curve0, y_curve0, y_curve1, y_curve2, cnt2
    if is_play:
        tx_step.set_text("Step=" + str(cnt2))
        cnt += 1
        if cnt % 2 == 0:
            cnt2 += 1
            next_generation_ball1()
        next_generation_dot0()
        next_generation_ball0()
        next_generation_ball2()
        update_ball()
        y_curve0_roll = np.roll(y_curve0, 1)
        y_curve0 = y_curve0_roll
        y_curve0[0] = y_ball0
        curve0.set_ydata(y_curve0)
        y_curve1_roll = np.roll(y_curve1, 1)
        y_curve1 = y_curve1_roll
        y_curve1[1] = y_ball1
        curve1.set_ydata(y_curve1)
        y_curve2_roll = np.roll(y_curve2, 1)
        y_curve2 = y_curve2_roll
        y_curve2[0] = y_ball2
        curve2.set_ydata(y_curve2)
        print(y_ball0, y_ball1, y_ball2)


# Global variables
# Coordination
x_min = -20.
x_max = 20.
y_min = -10.
y_max = 10.

# Parameters
mass = 200.
mass_init = mass
k = 1.
k_init = k

omega = np.sqrt(k/mass)

amplitude = 5.

x_ball0 = 0.
y_ball0 = amplitude
x_dot0 = 0.
y_dot0 = y_ball0

x_ball1 = -10.
y_ball1 = amplitude
v_ball1 = 0.

x_ball2 = -15.
y_ball2 = amplitude
v_ball2 = 0.
flag_ball2 = True

radius_ball = 0.5
radius_dot = radius_ball / 2.

# Animation control
cnt = 0
is_play = False
cnt2 = 0

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
circle = patches.Circle(xy=(0., 0.), radius=amplitude, color='gray', fill=False)
ax.add_patch(circle)
dot0 = patches.Circle(xy=(x_dot0, y_dot0), radius=radius_dot, color='gray')
ax.add_patch(dot0)

ball0 = patches.Circle(xy=(x_ball0, y_ball0), radius=radius_ball, color='blue')
ax.add_patch(ball0)
ball1 = patches.Circle(xy=(x_ball1, y_ball1), radius=radius_ball, color='orange')
ax.add_patch(ball1)
ball2 = patches.Circle(xy=(x_ball2, y_ball2), radius=radius_ball, color='green')
ax.add_patch(ball2)

line1, = ax.plot([x_ball1, x_ball1], [0., y_ball1], color='orange')
line2, = ax.plot([x_ball2, x_ball2], [0., y_ball2], color='green')

x_curve = np.linspace(0, x_max, 500)
y_curve0 = x_curve * 0.
curve0, = ax.plot(x_curve, y_curve0, linestyle='-', label="y=A*cos(omega*step)", color='blue')
y_curve1 = x_curve * 0.
curve1, = ax.plot(x_curve, y_curve1, linestyle='-', label="Simulation1(calculate a and v in same step)", color='orange')
y_curve2 = x_curve * 0.
curve2, = ax.plot(x_curve, y_curve2, linestyle='-', label="Simulation1(calculate a then v)", color='green')

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
    root, textvariable=var_m, format="%.1f", from_=1., to=200., increment=1.,
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
anim = animation.FuncAnimation(fig, update, interval=100)
root.bind('<Configure>', on_change_window)
root.mainloop()
