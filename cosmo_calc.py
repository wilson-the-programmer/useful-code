import tkinter as tk
from tkinter import ttk, filedialog


root = tk.Tk()
root.title("COSMOLAB")
root.geometry("400x600")
root.resizable(False, False)

background = "#10151b"
panel = "#18212a"
entry_background = "#080d12"
text_background = "#070b0f"
foreground = "#d7e2e8"
cyan = "#00d9ff"
orange = "#ff9d32"
green = "#53e39b"

root.configure(bg=background)

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "TCombobox",
    fieldbackground=entry_background,
    background=panel,
    foreground=foreground,
    arrowcolor=cyan,
    borderwidth=1
)

style.configure(
    "TRadiobutton",
    background=panel,
    foreground=foreground,
    font=("TkDefaultFont", 9)
)

title = tk.Label(
    root,
    text="◈  COSMOLAB  ◈",
    bg=background,
    fg=cyan,
    font=("Arial", 20, "bold")
)
title.pack(pady=(12, 2))

subtitle = tk.Label(
    root,
    text="COSMOLOGY / PHYSICS INSTRUMENT",
    bg=background,
    fg="#71808a",
    font=("Arial", 8)
)
subtitle.pack(pady=(0, 10))

instrument = tk.Frame(
    root,
    bg=panel,
    highlightbackground="#31404b",
    highlightthickness=1
)
instrument.pack(fill="x", padx=12)

constant_label = tk.Label(
    instrument,
    text="PHYSICS CONSTANT",
    bg=panel,
    fg=orange,
    font=("Arial", 9, "bold")
)
constant_label.pack(anchor="w", padx=10, pady=(10, 3))

constants = {
    "Speed of light c": "299792458",
    "Gravitational constant G": "6.67430e-11",
    "Planck constant h": "6.62607015e-34",
    "Boltzmann constant k": "1.380649e-23",
    "Electron mass": "9.1093837e-31",
    "Proton mass": "1.6726219e-27",
    "Astronomical unit AU": "149597870700",
    "Parsec": "3.0856776e16"
}

constant_box = ttk.Combobox(
    instrument,
    values=list(constants.keys()),
    state="readonly",
    font=("Arial", 9)
)
constant_box.pack(fill="x", padx=10, pady=(0, 10))


def insert_constant(event=None):
    selected = constant_box.get()

    if selected in constants:
        input_entry.delete(0, tk.END)
        input_entry.insert(0, constants[selected])
        calculate()


constant_box.bind("<<ComboboxSelected>>", insert_constant)


input_label = tk.Label(
    instrument,
    text="INPUT VALUE",
    bg=panel,
    fg=cyan,
    font=("Arial", 9, "bold")
)
input_label.pack(anchor="w", padx=10)

input_entry = tk.Entry(
    instrument,
    bg=entry_background,
    fg=foreground,
    insertbackground=cyan,
    relief="flat",
    font=("Courier New", 14),
    highlightthickness=1,
    highlightbackground="#31404b",
    highlightcolor=cyan
)
input_entry.pack(fill="x", padx=10, pady=(3, 8), ipady=5)


mode = tk.StringVar(value="km_miles")

radio_frame = tk.Frame(instrument, bg=panel)
radio_frame.pack(fill="x", padx=8, pady=2)

tk.Radiobutton(
    radio_frame,
    text="KM → MILES",
    variable=mode,
    value="km_miles",
    command=lambda: calculate(),
    bg=panel,
    fg=foreground,
    selectcolor=background,
    activebackground=panel,
    activeforeground=cyan
).pack(side="left")

tk.Radiobutton(
    radio_frame,
    text="MILES → KM",
    variable=mode,
    value="miles_km",
    command=lambda: calculate(),
    bg=panel,
    fg=foreground,
    selectcolor=background,
    activebackground=panel,
    activeforeground=cyan
).pack(side="left")


result_label = tk.Label(
    instrument,
    text="RESULT",
    bg=panel,
    fg=green,
    font=("Arial", 9, "bold")
)
result_label.pack(anchor="w", padx=10, pady=(8, 3))

result_entry = tk.Entry(
    instrument,
    bg="#07120d",
    fg=green,
    insertbackground=green,
    relief="flat",
    font=("Courier New", 14),
    highlightthickness=1,
    highlightbackground="#294936",
    highlightcolor=green
)
result_entry.pack(fill="x", padx=10, pady=(0, 10), ipady=5)


def calculate(event=None):
    value = input_entry.get().strip()

    try:
        number = float(value)
    except ValueError:
        result_entry.delete(0, tk.END)
        return

    if mode.get() == "km_miles":
        result = number * 0.621371192237
    else:
        result = number * 1.609344

    result_entry.delete(0, tk.END)
    result_entry.insert(0, f"{result:.9g}")


input_entry.bind("<KeyRelease>", calculate)


button_frame = tk.Frame(root, bg=background)
button_frame.pack(pady=10)

button_style = {
    "bg": "#202c35",
    "fg": cyan,
    "activebackground": "#30414d",
    "activeforeground": "#ffffff",
    "relief": "flat",
    "font": ("Arial", 9, "bold"),
    "width": 10
}

tk.Button(
    button_frame,
    text="CALCULATE",
    command=calculate,
    **button_style
).grid(row=0, column=0, padx=3)

tk.Button(
    button_frame,
    text="CLEAR",
    command=lambda: (
        input_entry.delete(0, tk.END),
        result_entry.delete(0, tk.END)
    ),
    **button_style
).grid(row=0, column=1, padx=3)


notes_frame = tk.Frame(
    root,
    bg=panel,
    highlightbackground="#31404b",
    highlightthickness=1
)
notes_frame.pack(padx=12, pady=(0, 8))

notes_header = tk.Frame(notes_frame, bg=panel)
notes_header.pack(fill="x")

notes_label = tk.Label(
    notes_header,
    text="SCIENTIFIC SCRATCHPAD",
    bg=panel,
    fg=orange,
    font=("Arial", 9, "bold")
)
notes_label.pack(side="left", padx=8, pady=6)

text_widget = tk.Text(
    notes_frame,
    width=25,
    height=8,
    bg=text_background,
    fg=foreground,
    insertbackground=cyan,
    relief="flat",
    font=("Courier New", 9),
    wrap="word"
)
text_widget.pack(padx=8, pady=(0, 8))


def open_file():
    filename = filedialog.askopenfilename(
        filetypes=[
            ("Text files", "*.txt"),
            ("All files", "*.*")
        ]
    )

    if not filename:
        return

    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()

    text_widget.delete("1.0", tk.END)
    text_widget.insert("1.0", content)


def save_file():
    filename = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[
            ("Text files", "*.txt"),
            ("All files", "*.*")
        ]
    )

    if not filename:
        return

    content = text_widget.get("1.0", tk.END)

    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)


file_button_frame = tk.Frame(root, bg=background)
file_button_frame.pack()

tk.Button(
    file_button_frame,
    text="OPEN",
    command=open_file,
    **button_style
).pack(side="left", padx=3)

tk.Button(
    file_button_frame,
    text="SAVE",
    command=save_file,
    **button_style
).pack(side="left", padx=3)


status = tk.Label(
    root,
    text="SYSTEM READY  •  COSMOLOGY MODULE ONLINE",
    bg=background,
    fg="#596a74",
    font=("Courier New", 7)
)
status.pack(pady=8)

root.mainloop()

