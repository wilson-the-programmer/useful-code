import tkinter as tk
from tkinter import filedialog, messagebox
import math

root = tk.Tk()
root.config(bg="cyan")
root.title("Measurement Converter")
root.geometry("1060x1100")

# ---------- Global unit selection ----------
input_unit = "Miles"  # default

# Conversion factors to meters
LENGTH_CONVERSION_FACTORS = {
    "Miles": 1609.344,
    "Kilometers": 1000.0,
    "Meters": 1.0,
    "Centimeters": 0.01,
    "Millimeters": 0.001,
    "Feet": 0.3048,
    "Inches": 0.0254,
    "Yards": 0.9144,
    "Nautical miles": 1852.0,
    "Micrometers": 1e-6,
}

UNIT_ORDER = list(LENGTH_CONVERSION_FACTORS.keys())  # nice display order


def set_input_unit(unit):
    """Called by the Units menu."""
    global input_unit
    input_unit = unit
 
    convert()  # recalculate immediately


def convert(event=None):
    output_window.delete("1.0", tk.END)

    try:
        value = eval(input_window.get("insert linestart", "insert").strip())
    except:
        pass

    if not value:
        return

    try:
        value = float(value)
        if not math.isfinite(value):
            raise ValueError

        # Convert the entered value to meters, then to every unit
        meters = value * LENGTH_CONVERSION_FACTORS[input_unit]

        for name in UNIT_ORDER:
            result = meters / LENGTH_CONVERSION_FACTORS[name]
            output_window.insert(tk.END, f"{name:<18} {result:,.6g}\n")
            middle_window.delete(1.0, "end")
            middle_window.insert(1.0, value)

    except ValueError:
        output_window.insert(tk.END, "Please enter a valid number.")
        
        


def open_file():
    filename = filedialog.askopenfilename(
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if filename:
        try:
            with open(filename, "r", encoding="utf-8") as file:
                input_window.delete("1.0", tk.END)
                input_window.insert("1.0", file.read())
                convert()
        except OSError as error:
            messagebox.showerror("Open Error", str(error))


def save_file():
    filename = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
    )
    if filename:
        try:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(input_window.get("1.0", tk.END).rstrip())
        except OSError as error:
            messagebox.showerror("Save Error", str(error))


def clear_input():
    input_window.delete("1.0", tk.END)
    output_window.delete("1.0", tk.END)
    input_window.focus_set()


# ---------- UI ----------
main_frame = tk.Frame(
    root,
    bg="grey",
    padx=12,
    pady=12
)

main_frame.pack(fill=tk.BOTH, expand=True)


input_window = tk.Text(
    main_frame,
    height=6,
    font=("Courier New", 8),
    bd=10,
    bg="#112244",
    fg="lightgrey",
    insertbackground="cyan",
    insertwidth=5,
    wrap="word",
    padx=10,
    pady=10
)
input_window.pack(fill=tk.BOTH, expand=True, pady=(5, 15))


middle_window = tk.Text(
    main_frame,
    height=1,
    bd=5,
    font=("Courier New", 8),
    wrap="word",
    bg="black",
    fg="lightgrey",
    insertbackground="orange",
    insertwidth=5,
    padx=10
)
middle_window.pack(
    fill="both",
    expand=True,
    pady=5
)

output_window = tk.Text(
    main_frame,
    height=12,
    bg="darkblue",
    fg="white",
    insertbackground="cyan",
    padx=10,
    pady=10,
    insertwidth=5,
    font=("Courier New", 8),
    wrap="word"
)
output_window.pack(
    fill="both",
    expand=True,
    pady=5
)

# ---------- Menus ----------
menu_bar = tk.Menu(
    root,
    font=("Courier New", 12),
    bg="black",
    fg="lightgrey"
)

# File menu
file_menu = tk.Menu(
    menu_bar,
    font=("Courier New", 11),
    bg="lightyellow",
    fg="#000095"
)

file_menu.add_command(label="Open", command=open_file)

file_menu.add_command(label="Save", command=save_file)

file_menu.add_separator()

file_menu.add_command(label="Clear", command=clear_input)


file_menu.add_command(label="Exit", command=root.destroy)

menu_bar.add_cascade(label="File", menu=file_menu)

# Units menu
units_menu = tk.Menu(
    menu_bar,
    font=("Courier New", 11),
    bg="black",
    fg="lightgrey"
)

for unit in UNIT_ORDER:
    units_menu.add_command(label=unit, command=lambda u=unit: set_input_unit(u))
menu_bar.add_cascade(label="Units", menu=units_menu)

root.config(menu=menu_bar)

input_window.bind("<KeyRelease>", convert)


input_window.bind("<Button-1>", convert)


input_window.focus_set()

root.mainloop()
