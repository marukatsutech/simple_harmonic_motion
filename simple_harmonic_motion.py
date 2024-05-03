# Simple harmonic motion
import tkinter
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import matplotlib.animation as animation
import numpy as np
import matplotlib.patches as patches


def draw_spring(xs1, xs2, turn_spring, half_width_spring):
    x_start = min(xs1, xs2)
    x_end = max(xs1, xs2)
    len_spring = abs(x_start - x_end)
    pitch_spring = len_spring / turn_spring
    # Draw 1st line
    ax.plot([x_start, x_start + pitch_spring / 4], [0., half_width_spring], c='black')
    # Draw last line
    ax.plot([x_end, x_end - pitch_spring / 4], [0., - half_width_spring], c='black')
    # Draw other lines
    for i in range(turn_spring):
        xo_start = x_start + pitch_spring * i + pitch_spring / 4
        ax.plot([xo_start, xo_start + pitch_spring * 2 / 4], [half_width_spring, - half_width_spring], c='black')
    for i in range(turn_spring - 1):
        xo_start = x_start + pitch_spring * i + pitch_spring * 3 / 4
        ax.plot([xo_start, xo_start + pitch_spring * 2 / 4], [- half_width_spring, half_width_spring], c='black')


def on_button_release(event):
    global in_drag, force, a, v
    in_drag = False
    force = 0.
    a = 0.
    v = 0.


def on_button_press(event):
    global in_drag
    if event.button == 1:
        in_drag = True


def motion(event):
    global x_ball, y_ball
    if (event.xdata is None) or (event.ydata is None):
        return
    if in_drag:
        x_ball = event.xdata
        if x_ball > x_limit:
            x_ball = x_limit
        if x_ball < - x_limit:
            x_ball = - x_limit


def change_k(value):
    global k
    k = float(value)


def change_m(value):
    global mass
    mass = float(value)


def stop():
    global force, a, v, x_ball
    force = 0.
    a = 0.
    v = 0.
    x_ball = 0.


def set_axis():
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_title('Simple harmonic motion')
    ax.set_xlabel('x')
    tm_adjust = resolution / y_max  # To adjust time scale and line-space
    ax.set_ylabel('t * ' + str(f'{tm_adjust:.1f}'))
    ax.grid()
    ax.set_aspect("equal")


def update(f):
    ax.cla()  # Clear ax
    set_axis()

    global x_ball, y_ball, force, a, v, x
    ax.text(x_min, y_max * 0.9, " Step(as t)=" + str(f))
    freq = 1 / (2 * np.pi) * np.sqrt(k / mass)
    ax.text(x_min, y_max * 0.8, " f(=1/2pi*sqr(k/m))=" + str(f'{freq:.3f}'))
    time_period = 1 / freq
    ax.text(x_min, y_max * 0.7, " T(=1/f)=" + str(f'{time_period:.3f}'))
    # Draw ball
    c = patches.Circle(xy=(x_ball, y_ball), radius=radius_ball, fc='black', ec='black')
    ax.add_patch(c)
    # Draw line
    x_roll = np.roll(x, 1)
    x = x_roll
    x[0] = x_ball
    ax.plot(x, y, label="dx")
    ax.legend(prop={"size": 8}, loc="best")
    # Draw spring
    draw_spring(x_min, x_ball - radius_ball, turn_s, half_ws)
    # Draw explanations
    ax.text(x_ball, y_max * 0.2, "m")
    ax.text((x_ball + x_min) / 2, y_max * 0.2, "k")
    ax.plot([x_ball, x_ball], [0., y_min], c='black', linewidth='1', linestyle=':')
    ax.text(x_ball, y_min * 0.4, "dx=" + str(f'{x_ball:.2f}'))
    ax.annotate(
        '', xy=[x_ball, y_min * 0.5], xytext=[0., y_min * 0.5],
        arrowprops=dict(width=1, headwidth=4, headlength=4, facecolor='blue', edgecolor='blue')
        )
    allow_f_len = force
    ax.text(x_ball, y_min * 0.7, "F(=-k*dx)=" + str(f'{force:.2f}'))
    ax.annotate(
        '', xy=[x_ball + allow_f_len, y_min * 0.8], xytext=[x_ball, y_min * 0.8],
        arrowprops=dict(width=1, headwidth=4, headlength=4, facecolor='red', edgecolor='red')
        )
    # Calculate motion of a ball
    if not in_drag:
        force = - k * x_ball
        a = force / mass
        v = v + a
        x_ball = x_ball + v


# Global variables
x_min = -4.
x_max = 4.
y_min = -2.
y_max = 4.

in_drag = False

# Parameters
x_ball = 0.
y_ball = 0.
k = 1.
mass = 50.
x_limit = 3.
radius_ball = 0.5
turn_s = 6     # Turn of spring
half_ws = 0.4   # Half width of spring

force = 0.
a = 0.
v = 0.

# Generate Line space
resolution = 200
y = np.linspace(0, y_max, resolution)
x = y * 0.

# Generate tkinter
root = tkinter.Tk()
root.title("Simple harmonic motion")

# Generate figure and axes
fig = Figure(figsize=(6, 4))
fig.canvas.mpl_connect('motion_notify_event', motion)
fig.canvas.mpl_connect('button_press_event', on_button_press)
fig.canvas.mpl_connect('button_release_event', on_button_release)
ax = fig.add_subplot(111)

# Embed a figure in canvas
canvas = FigureCanvasTkAgg(fig, root)
canvas.get_tk_widget().pack(expand=True, fill='both')

# Animation
anim = animation.FuncAnimation(fig, update, interval=100, save_count=100)

# Toolbar
toolbar = NavigationToolbar2Tk(canvas, root)
canvas.get_tk_widget().pack()

# Label and spinbox for k (spring constant)
label_k = tkinter.Label(root, text="k(Spring constant)")
label_k.pack(side='left')
var_k = tkinter.StringVar(root)  # variable for spinbox-value
var_k.set(k)  # Initial value
s_k = tkinter.Spinbox(
    root, textvariable=var_k, format="%.1f", from_=0.1, to=2.0, increment=0.1,
    command=lambda: change_k(var_k.get()), width=4
    )
s_k.pack(side='left')
# Label and spinbox for mass
label_m = tkinter.Label(root, text=", m(Mass)")
label_m.pack(side='left')
var_m = tkinter.StringVar(root)  # variable for spinbox-value
var_m.set(mass)  # Initial value
s_m = tkinter.Spinbox(
    root, textvariable=var_m, format="%.1f", from_=50., to=100., increment=1,
    command=lambda: change_m(var_m.get()), width=4
    )
s_m.pack(side='left')
# Label
m = tkinter.Label(root, relief="sunken", text='Drag the ball to start!')
m.pack(side='left')
# Reset button
b = tkinter.Button(root, text="Stop", command=stop)
b.pack(side='left')

# main loop
set_axis()
tkinter.mainloop()
