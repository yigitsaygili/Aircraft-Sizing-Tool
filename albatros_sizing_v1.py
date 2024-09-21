import tkinter as tk
from tkinter import ttk
import math
from PIL import Image, ImageTk
import webbrowser
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

def open_link(event):
    webbrowser.open_new("https://github.com/yigitsaygili")

def calculate():
    # INPUTS
    weigth = float(weigth_spinbox.get())
    wing_area = float(wing_area_spinbox.get())
    airspeed = float(airspeed_spinbox.get())
    cl = float(cl_spinbox.get())
    cl_max = float(cl_max_spinbox.get())
    cd = float(cd_spinbox.get())
    aspect_ratio = float(aspect_ratio_spinbox.get())
    taper_ratio = float(taper_ratio_spinbox.get())
    center_gravity = float(center_gravity_spinbox.get())
    neutral_point = float(neutral_point_spinbox.get())

    ht_coefficient = float(ht_coefficient_spinbox.get())
    ht_arm = float(ht_arm_spinbox.get())
    ht_aspect_ratio = float(ht_aspect_ratio_spinbox.get())
    ht_taper_ratio = float(ht_ytaper_ratio_spinbox.get())
    vt_coefficient = float(vt_coefficient_spinbox.get())
    vt_arm = float(vt_arm_spinbox.get())
    vt_aspect_ratio = float(vt_aspect_ratio_spinbox.get())
    vt_taper_ratio  = float(vt_taper_ratio_spinbox.get())

    # CONSTANTS
    rho = 1.225
    gravity = 9.81
    
    # WING DESIGN
    wing_span = math.sqrt(wing_area*aspect_ratio)
    mean_chord = wing_area/wing_span
    root_coord = (3/2)*mean_chord*((1+taper_ratio)/(taper_ratio+1+taper_ratio*taper_ratio))
    tip_coord = taper_ratio*root_coord

    # LIFT AND SPEED
    lift = (0.5*rho*airspeed*airspeed)*wing_area*cl / gravity
    cruise_speed = math.sqrt((2*gravity*weigth)/(cl*rho*wing_area))
    stall_speed = math.sqrt((2*gravity*weigth)/(cl_max*rho*wing_area))

    # DRAG
    drag = (0.5*rho*airspeed*airspeed)*wing_area*cd / gravity
    oswald_factor = 0.85 #1.78*(1-(0.045*(aspect_ratio^0.68)))-0.64
    cd_ind = cd+((cl*cl)/(math.pi*oswald_factor*aspect_ratio))
    induced_drag = (0.5*rho*airspeed*airspeed)*wing_area*cd_ind / gravity

    # WEIGHT AND STABILITY
    static_margin =((neutral_point-center_gravity)/mean_chord)*100
    wing_loading = weigth/wing_area
    cubic_loading = weigth/ (wing_area*math.sqrt(wing_area))

    # HORIZONTAL AND VERTICAL TAIL
    ht_area = (ht_coefficient*wing_area*mean_chord)/ht_arm
    ht_span = math.sqrt(ht_area*ht_aspect_ratio)
    ht_mean_chord = ht_area/ht_span
    ht_root_chord = (3/2)*ht_mean_chord*((1+ht_taper_ratio)/(ht_taper_ratio+1+ht_taper_ratio*ht_taper_ratio))
    ht_tip_chord = ht_root_chord*ht_taper_ratio
    vt_area = (vt_coefficient*wing_area*wing_span)/vt_arm
    vt_span = math.sqrt(vt_area*vt_aspect_ratio)
    vt_mean_chord = vt_area/vt_span
    vt_root_chord = (3/2)*vt_mean_chord*((1+vt_taper_ratio)/(vt_taper_ratio+1+vt_taper_ratio*vt_taper_ratio))
    vt_tip_chord = vt_root_chord*vt_taper_ratio
    wing_tail_ratio = (ht_area/wing_area)*100

    # Update output labels
    wing_span_label.config(text=f"Wing Span [m]: {wing_span:.2f}")
    mean_chord_label.config(text=f"Mean Chord [m]: {mean_chord:.2f}")
    root_chord_label.config(text=f"Root Chord [m]: {root_coord:.2f}")
    tip_chord_label.config(text=f"Tip Chord [m]: {tip_coord:.2f}")

    lift_label.config(text=f"Lift [kg]: {lift:.2f}")
    cruise_speed_label.config(text=f"Cruise Speed [m/s]: {cruise_speed:.2f}")
    stall_speed_label.config(text=f"Stall Speed [m/s]: {stall_speed:.2f}")
    drag_label.config(text=f"Drag [kg]: {drag:.2f}")
    induced_drag_label.config(text=f"Induced Drag [kg]: {induced_drag:.2f}")

    wing_loading_label.config(text=f"Wing Loading: {wing_loading:.2f}")
    cubic_loading_label.config(text=f"Cubic Loading: {cubic_loading:.2f}")

    ht_area_label.config(text=f"HT Area [m2]: {ht_area:.2f}")
    ht_span_label.config(text=f"HT Span [m]: {ht_span:.2f}")
    ht_mean_chord_label.config(text=f"HT Mean Chord [m]: {ht_mean_chord:.2f}")
    ht_root_chord_label.config(text=f"HT Root Chord [m]: {ht_root_chord:.2f}")
    ht_tip_chord_label.config(text=f"HT Tip Chord [m]: {ht_tip_chord:.2f}")

    vt_area_label.config(text=f"VT Area [m2]: {vt_area:.2f}")
    vt_span_label.config(text=f"VT Span [m]: {vt_span:.2f}")
    vt_mean_chord_label.config(text=f"VT Mean Chord [m]: {vt_mean_chord:.2f}")
    vt_root_chord_label.config(text=f"VT Root Chord [m]: {vt_root_chord:.2f}")
    vt_tip_chord_label.config(text=f"VT Tip Chord [m]: {vt_tip_chord:.2f}")

    static_margin_label.config(text=f"Static Margin: {static_margin:.2f}")
    wing_tail_ratio_label.config(text=f"Wing/Tail Ratio: {wing_tail_ratio:.2f}")

    ax1.clear()  # Clear the existing plot
    x_values = [0, wing_span, wing_span, 0, 0, ht_span, ht_span, 0]
    y_values = [0, -(root_coord-tip_coord)/2, -tip_coord-(root_coord-tip_coord)/2, -root_coord, -root_coord-ht_arm, -root_coord-ht_arm-(ht_root_chord-ht_tip_chord)
                , -root_coord-ht_arm-(ht_root_chord-ht_tip_chord)-ht_tip_chord, -root_coord-ht_arm-ht_root_chord]
    ax1.plot(x_values, y_values)
    ax1.plot(-1 * np.array(x_values), y_values)
    ax1.plot(0, -center_gravity, 'ko')
    ax1.plot(0, -neutral_point, 'ko')
    ax1.text(0.25, -center_gravity, "CoG", ha='center', fontsize=10, color='black')
    ax1.text(0.25, -neutral_point, "NP", ha='center', fontsize=10, color='black')
    ax1.axis('off')
    canvas1.draw()  # Redraw the canvas

    return


# GUI OPERATIONS
root = tk.Tk()
root.title("Albatros Aircraft Sizing")
root.resizable(False, False)  # Disable resizing

# Create a ttk.Style object
style = ttk.Style()
style.theme_use('clam')  # You can try 'alt', 'default', 'classic', etc.

# Load the image
image = Image.open("albatros.jpg")  # Specify the path to your image
photo = ImageTk.PhotoImage(image)
image_label = tk.Label(root, image=photo)
image_label.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

# Frame for upper surface coefficients
intro_frame = tk.Frame(root)
intro_frame.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky='nsew')
tk.Label(intro_frame, text="ITU Albatros UAV Team - Aerodynamics Department 2024").pack(anchor='w')
tk.Label(intro_frame, text="Aircraft Sizing Tool\n").pack(anchor='w')
tk.Label(intro_frame, text="Use iteratively coupled with XFLR5 Plane Design tab").pack(anchor='w')

# Add single "Calculate All" button at the bottom
calc_button = tk.Button(root, text="Calculate", command=calculate, bg='#2b54ca', fg='white', font=('Arial',10,'bold'))
calc_button.grid(row=4, column=0, padx=10, pady=10, sticky='nsew')
wing_span, mean_chord, root_coord, tip_coord, lift, cruise_speed, stall_speed, drag, induced_drag, static_margin, wing_loading, cubic_loading = [0,0,0,0,0,0,0,0,0,0,0,0]
ht_area, ht_span, ht_mean_chord, ht_root_chord, ht_tip_chord, vt_area, vt_span, vt_mean_chord, vt_root_chord, vt_tip_chord, wing_tail_ratio = [0,0,0,0,0,0,0,0,0,0,0]


# INPUTS PANEL
inputs_panel = tk.LabelFrame(root, text="INPUTS", padx=10, pady=10, font=('Arial', 10, 'bold'))
inputs_panel.grid(row=1, column=0, rowspan=3, padx=10, pady=10, sticky='nsew')

tk.Label(inputs_panel, text="Weigth [kg]:", anchor='w').grid(row=0, column=0, sticky='w')
tk.Label(inputs_panel, text="Wing Area [m2]:", anchor='w').grid(row=1, column=0, sticky='w')
tk.Label(inputs_panel, text="Airspeed [m/s]:", anchor='w').grid(row=2, column=0, sticky='w')
tk.Label(inputs_panel, text="Lift Coefficient:", anchor='w').grid(row=3, column=0, sticky='w')
tk.Label(inputs_panel, text="Max Lift Coefficient:", anchor='w').grid(row=4, column=0, sticky='w')
tk.Label(inputs_panel, text="Drag Coefficient:", anchor='w').grid(row=5, column=0, sticky='w')
tk.Label(inputs_panel, text="Wing Aspect Ratio:", anchor='w').grid(row=6, column=0, sticky='w')
tk.Label(inputs_panel, text="Wing Taper Ratio:", anchor='w').grid(row=7, column=0, sticky='w')
tk.Label(inputs_panel, text="Center of Gravity [m]:", anchor='w').grid(row=8, column=0, sticky='w')
tk.Label(inputs_panel, text="Neutral Point [m]:", anchor='w').grid(row=9, column=0, sticky='w')

tk.Label(inputs_panel, text=" ", anchor='w').grid(row=10, column=0, columnspan=2, sticky='w')
tk.Label(inputs_panel, text="Horizontal Tail Coefficient:", anchor='w').grid(row=11, column=0, sticky='w')
tk.Label(inputs_panel, text="Horizontal Tail Arm:", anchor='w').grid(row=12, column=0, sticky='w')
tk.Label(inputs_panel, text="Horizontal Tail Aspect Ratio:", anchor='w').grid(row=13, column=0, sticky='w')
tk.Label(inputs_panel, text="Horizontal Tail Taper Ratio:", anchor='w').grid(row=14, column=0, sticky='w')
tk.Label(inputs_panel, text="Vertical Tail Coefficient:", anchor='w').grid(row=15, column=0, sticky='w')
tk.Label(inputs_panel, text="Vertical Tail Arm:", anchor='w').grid(row=16, column=0, sticky='w')
tk.Label(inputs_panel, text="Vertical Tail Aspect Ratio:", anchor='w').grid(row=17, column=0, sticky='w')
tk.Label(inputs_panel, text="Vertical Tail Taper Ratio:", anchor='w').grid(row=18, column=0, sticky='w')

# Adjust the width and font size of the Spinbox
weigth_spinbox = tk.Spinbox(inputs_panel, from_=0, to=100, increment=0.01, width=5, font=('Arial', 10), value=10.0)
wing_area_spinbox = tk.Spinbox(inputs_panel, from_=0, to=100, increment=0.01, width=5, font=('Arial', 10), value=0.8)
airspeed_spinbox = tk.Spinbox(inputs_panel, from_=0, to=100, increment=0.01, width=5, font=('Arial', 10), value=20.0)
cl_spinbox = tk.Spinbox(inputs_panel, from_=0, to=100, increment=0.01, width=5, font=('Arial', 10), value=0.45)
cl_max_spinbox = tk.Spinbox(inputs_panel, from_=0, to=100, increment=0.01, width=5, font=('Arial', 10), value=1.25)
cd_spinbox = tk.Spinbox(inputs_panel, from_=0, to=100, increment=0.01, width=5, font=('Arial', 10), value=0.05)
aspect_ratio_spinbox = tk.Spinbox(inputs_panel, from_=0, to=100, increment=0.01, width=5, font=('Arial', 10), value=6.5)
taper_ratio_spinbox = tk.Spinbox(inputs_panel, from_=0, to=100, increment=0.01, width=5, font=('Arial', 10), value=0.5)
center_gravity_spinbox = tk.Spinbox(inputs_panel, from_=0, to=100, increment=0.01, width=5, font=('Arial', 10), value=0.25)
neutral_point_spinbox = tk.Spinbox(inputs_panel, from_=0, to=100, increment=0.01, width=5, font=('Arial', 10), value=0.35)

ht_coefficient_spinbox = tk.Spinbox(inputs_panel, from_=0, to=100, increment=0.01, width=5, font=('Arial', 10), value=0.5)
ht_arm_spinbox = tk.Spinbox(inputs_panel, from_=0, to=100, increment=0.01, width=5, font=('Arial', 10), value=0.75)
ht_aspect_ratio_spinbox = tk.Spinbox(inputs_panel, from_=0, to=100, increment=0.01, width=5, font=('Arial', 10), value=3.5)
ht_ytaper_ratio_spinbox = tk.Spinbox(inputs_panel, from_=0, to=100, increment=0.01, width=5, font=('Arial', 10), value=0.5)
vt_coefficient_spinbox = tk.Spinbox(inputs_panel, from_=0, to=100, increment=0.01, width=5, font=('Arial', 10), value=0.05)
vt_arm_spinbox = tk.Spinbox(inputs_panel, from_=0, to=100, increment=0.01, width=5, font=('Arial', 10), value=0.75)
vt_aspect_ratio_spinbox = tk.Spinbox(inputs_panel, from_=0, to=100, increment=0.01, width=5, font=('Arial', 10), value=1.5)
vt_taper_ratio_spinbox = tk.Spinbox(inputs_panel, from_=0, to=100, increment=0.01, width=5, font=('Arial', 10), value=0.5)

weigth_spinbox.grid(row=0, column=1)
wing_area_spinbox.grid(row=1, column=1)
airspeed_spinbox.grid(row=2, column=1)
cl_spinbox.grid(row=3, column=1)
cl_max_spinbox.grid(row=4, column=1)
cd_spinbox.grid(row=5, column=1)
aspect_ratio_spinbox.grid(row=6, column=1)
taper_ratio_spinbox.grid(row=7, column=1)
center_gravity_spinbox.grid(row=8, column=1)
neutral_point_spinbox.grid(row=9, column=1)

ht_coefficient_spinbox.grid(row=11, column=1)
ht_arm_spinbox.grid(row=12, column=1)
ht_aspect_ratio_spinbox.grid(row=13, column=1)
ht_ytaper_ratio_spinbox.grid(row=14, column=1)
vt_coefficient_spinbox.grid(row=15, column=1)
vt_arm_spinbox.grid(row=16, column=1)
vt_aspect_ratio_spinbox.grid(row=17, column=1)
vt_taper_ratio_spinbox.grid(row=18, column=1)


# WING DESIGN PANEL
wing_panel = tk.LabelFrame(root, text="Wing Design", padx=10, pady=10, font=('Arial', 10, 'bold'))
wing_panel.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

wing_span_label = tk.Label(wing_panel, text=f"Wing Span [m]: {wing_span:.2f}", anchor='w')
mean_chord_label = tk.Label(wing_panel, text=f"Mean Chord [m]: {mean_chord:.2f}", anchor='w')
root_chord_label = tk.Label(wing_panel, text=f"Root Chord [m]: {root_coord:.2f}", anchor='w')
tip_chord_label = tk.Label(wing_panel, text=f"Tip Chord [m]: {tip_coord:.2f}", anchor='w')

wing_span_label.grid(row=2, column=0, columnspan=2, sticky='w')
mean_chord_label.grid(row=3, column=0, columnspan=2, sticky='w')
root_chord_label.grid(row=4, column=0, columnspan=2, sticky='w')
tip_chord_label.grid(row=5, column=0, columnspan=2, sticky='w')


# LIFT AND DRAG PANEL
lift_drag_panel = tk.LabelFrame(root, text="Lift and Drag", padx=10, pady=10, font=('Arial', 10, 'bold'))
lift_drag_panel.grid(row=2, column=1, padx=10, pady=10, sticky='nsew')

lift_label = tk.Label(lift_drag_panel, text=f"Lift [kg]: {lift:.2f}", anchor='w')
cruise_speed_label = tk.Label(lift_drag_panel, text=f"Cruise Speed [m/s]: {cruise_speed:.2f}", anchor='w')
stall_speed_label = tk.Label(lift_drag_panel, text=f"Stall Speed [m/s]: {stall_speed:.2f}", anchor='w')
drag_label = tk.Label(lift_drag_panel, text=f"Drag [kg]: {drag:.2f}", anchor='w')
induced_drag_label = tk.Label(lift_drag_panel, text=f"Induced Drag [kg]: {induced_drag:.2f}", anchor='w')

lift_label.grid(row=2, column=0, columnspan=2, sticky='w')
cruise_speed_label.grid(row=3, column=0, columnspan=2, sticky='w')
stall_speed_label.grid(row=4, column=0, columnspan=2, sticky='w')
drag_label.grid(row=5, column=0, columnspan=2, sticky='w')
induced_drag_label.grid(row=6, column=0, columnspan=2, sticky='w')


# WING LOADING PANEL
loading_panel = tk.LabelFrame(root, text="Wing Loading", padx=10, pady=10, font=('Arial', 10, 'bold'))
loading_panel.grid(row=3, column=1, padx=10, pady=10, sticky='nsew')

wing_loading_label = tk.Label(loading_panel, text=f"Wing Loading: {wing_loading:.2f}", anchor='w')
cubic_loading_label = tk.Label(loading_panel, text=f"Cubic Loading: {cubic_loading:.2f}", anchor='w')

wing_loading_label.grid(row=2, column=0, columnspan=2, sticky='w')
cubic_loading_label.grid(row=3, column=0, columnspan=2, sticky='w')


# HORIZONTAL TAIL PANEL
ht_panel = tk.LabelFrame(root, text="Horizontal Tail", padx=10, pady=10, font=('Arial', 10, 'bold'))
ht_panel.grid(row=1, column=2, padx=10, pady=10, sticky='nsew')

ht_area_label = tk.Label(ht_panel, text=f"HT Area [m]: {ht_area:.2f}", anchor='w')
ht_span_label = tk.Label(ht_panel, text=f"HT Span [m]: {ht_span:.2f}", anchor='w')
ht_mean_chord_label = tk.Label(ht_panel, text=f"HT Mean Chord [m]: {ht_mean_chord:.2f}", anchor='w')
ht_root_chord_label = tk.Label(ht_panel, text=f"HT Root Chord [m]: {ht_root_chord:.2f}", anchor='w')
ht_tip_chord_label = tk.Label(ht_panel, text=f"HT Tip Chord [m]: {ht_tip_chord:.2f}", anchor='w')

ht_area_label.grid(row=2, column=0, columnspan=2, sticky='w')
ht_span_label.grid(row=3, column=0, columnspan=2, sticky='w')
ht_mean_chord_label.grid(row=4, column=0, columnspan=2, sticky='w')
ht_root_chord_label.grid(row=5, column=0, columnspan=2, sticky='w')
ht_tip_chord_label.grid(row=6, column=0, columnspan=2, sticky='w')


# VERTICAL TAIL PANEL
vt_panel = tk.LabelFrame(root, text="Vertical Tail", padx=10, pady=10, font=('Arial', 10, 'bold'))
vt_panel.grid(row=2, column=2, padx=10, pady=10, sticky='nsew')

vt_area_label = tk.Label(vt_panel, text=f"VT Area [m]: {vt_area:.2f}", anchor='w')
vt_span_label = tk.Label(vt_panel, text=f"VT Span [m]: {vt_span:.2f}", anchor='w')
vt_mean_chord_label = tk.Label(vt_panel, text=f"VT Mean Chord [m]: {vt_mean_chord:.2f}", anchor='w')
vt_root_chord_label = tk.Label(vt_panel, text=f"VT Root Chord [m]: {vt_root_chord:.2f}", anchor='w')
vt_tip_chord_label = tk.Label(vt_panel, text=f"VT Tip Chord [m]: {vt_tip_chord:.2f}", anchor='w')

vt_area_label.grid(row=2, column=0, columnspan=2, sticky='w')
vt_span_label.grid(row=3, column=0, columnspan=2, sticky='w')
vt_mean_chord_label.grid(row=4, column=0, columnspan=2, sticky='w')
vt_root_chord_label.grid(row=5, column=0, columnspan=2, sticky='w')
vt_tip_chord_label.grid(row=6, column=0, columnspan=2, sticky='w')


# STABILITY PANEL
stability_panel = tk.LabelFrame(root, text="Stability", padx=10, pady=10, font=('Arial', 10, 'bold'))
stability_panel.grid(row=3, column=2, padx=10, pady=10, sticky='nsew')

static_margin_label = tk.Label(stability_panel, text=f"Static Margin: {static_margin:.2f}", anchor='w')
wing_tail_ratio_label = tk.Label(stability_panel, text=f"Wing/Tail Ratio: {wing_tail_ratio:.2f}", anchor='w')

static_margin_label.grid(row=2, column=0, columnspan=2, sticky='w')
wing_tail_ratio_label.grid(row=3, column=0, columnspan=2, sticky='w')


# AIRCRAFT LAYOUT PANEL
layout_panel = tk.LabelFrame(root, text="Aircraft Layout", padx=10, pady=10, font=('Arial', 10, 'bold'))
layout_panel.grid(row=1, column=3, rowspan=3, padx=10, pady=10, sticky='nsew')

fig1 = plt.Figure(figsize=(5,3), dpi=100)
ax1 = fig1.add_subplot(111)
ax1.grid(True)
ax1.axis('off')
canvas1 = FigureCanvasTkAgg(fig1, master=layout_panel)
canvas1.draw()
canvas1.get_tk_widget().pack(fill='both', expand=True)


# Frame for footer
footer_frame = tk.Frame(root, padx=10, pady=10,)
footer_frame.grid(row=4, column=1, columnspan=2, sticky='nsew')
footer_label = tk.Label(footer_frame, text="Developed by Yigit with ❤️", fg="blue", cursor="hand2")
footer_label.pack()
footer_label.bind("<Button-1>", open_link)

# Start the GUI event loop
root.mainloop()
