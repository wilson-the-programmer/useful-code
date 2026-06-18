#

import io
import sys

import tkinter as tk

from tkinter import (
    filedialog,
    scrolledtext
)

import keyword
import re



def auto_indent(event=None):
    current_widget = root.focus_get()
    current_line = int(current_widget.index("insert").split(".")[0])
    start_of_line = f"{current_line}.0"
    text_contents = current_widget.get(start_of_line, start_of_line + " lineend")
    indentation = text_contents[: len(text_contents) - len(text_contents.lstrip())]
    if (
        indentation
        and current_line == int(current_widget.index("insert").split(".")[0])
    ):
        current_widget.insert("insert", "\n" + indentation)
        current_widget.see("insert")
        return "break"
    else:
        pass



def highlight_code(event=None):
    editor.tag_remove("kw", "1.0", "end")
    editor.tag_remove("var", "1.0", "end")
    editor.tag_remove("eq", "1.0", "end")
    editor.tag_remove("num", "1.0", "end")
    editor.tag_remove("str", "1.0", "end")
    editor.tag_remove("call", "1.0", "end")

    text = editor.get("1.0", "end-1c")

    for k in keyword.kwlist:
        start = "1.0"
        while True:
            pos = editor.search(rf"\y{k}\y", start, stopindex="end", regexp=True)
            if not pos:
                break
            end = f"{pos}+{len(k)}c"
            editor.tag_add("kw", pos, end)
            start = end

    for m in re.finditer(r"\b([A-Za-z_]\w*)\s*=", text):
        start = f"1.0+{m.start(1)}c"
        end = f"1.0+{m.end(1)}c"
        editor.tag_add("var", start, end)

    for m in re.finditer(r"=", text):
        p = f"1.0+{m.start()}c"
        editor.tag_add("eq", p, f"{p}+1c")

    for m in re.finditer(r"\b\d+(\.\d+)?\b", text):
        start = f"1.0+{m.start()}c"
        end = f"1.0+{m.end()}c"
        editor.tag_add("num", start, end)

    for m in re.finditer(r'".*?"|\'.*?\'', text):
        start = f"1.0+{m.start()}c"
        end = f"1.0+{m.end()}c"
        editor.tag_add("str", start, end)

    for m in re.finditer(r"\b([A-Za-z_]\w*)\(", text):
        start = f"1.0+{m.start(1)}c"
        end = f"1.0+{m.end(1)}c"
        editor.tag_add("call", start, end)

    editor.tag_config("kw", foreground="red")
    editor.tag_config("var", foreground="darkred")
    editor.tag_config("eq", foreground="purple")
    editor.tag_config("num", foreground="blue")
    editor.tag_config("str", foreground="green")
    editor.tag_config("call", foreground="darkred")


def run_python():
    current_widget = root.focus_get()
    code = current_widget.get("1.0", tk.END)

    output = io.StringIO()
    sys.stdout = output

    try:
        exec(code)

    except Exception as e:
        output.write(f"{type(e).__name__}: {e}")

    finally:
        sys.stdout = sys.__stdout__

        python_window = tk.Toplevel(root)
        python_window.geometry("450x350+0+0")
        
        python_window.title("Python Output")

        result_text = scrolledtext.ScrolledText(
            python_window,
            wrap="word",
            font=("Courier New", 8),
            height=5,
            bg="white",
            fg="black",
            padx=8,
            pady=8,
            bd=8,
            insertbackground="red",
            insertwidth=6
        )
        result_text.pack(
            fill="both",
            expand=True
        )

        result_text.insert("1.0", output.getvalue())
        
        exit_button = tk.Button(
            python_window,
            text="Exit",
            command=lambda: python_window.destroy(),
            font=("Courier New", 8),
            bd=5,
            width=2,
            bg="lightgrey",
            fg="darkblue" 
            
        )
        
        exit_button.pack(side="left")
        
        
        
   

def open_file():
    filename = filedialog.askopenfilename()

    if filename:
        with open(filename, "r", encoding="utf-8") as file:
            editor.delete("1.0", "end")
            editor.insert("1.0", file.read())


def save_file():
    filename = filedialog.asksaveasfilename(
        defaultextension=".txt"
    )

    if filename:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(editor.get("1.0", "end-1c"))
            

def clear_editor():
	editor.delete(1.0, "end")

def eval_exp():
    exp = editor.get("insert linestart", "insert lineend").strip()
    try:
        result = eval(exp)

        if isinstance(result, float):
            result = round(result, 3)

        editor.insert("insert", f" ≈ {result}")
        editor.event_generate("<Return>")
    except:
        pass
        


root = tk.Tk()
root.geometry("460x500+0+0")
editor = tk.Text(
    root,
    wrap="word",
    font=("Courier New", 8),
    height=5,
    bd=5,
    padx=8,
    pady=8,
    bg="white",
    fg="black",
    insertwidth=6,
    insertbackground="darkred"
)
editor.pack(
    expand=True,
    fill="both",
    side="top"
)


open_button = tk.Button(
    root,
    text="Open",
    font=("Times", 8, "bold"),
    bg="white",
    fg="blue",
    width=1,
    bd=6,
    command=open_file
)
open_button.pack(side="left")

save_button = tk.Button(
    root,
    text="Save",
    font=("Times", 8, "bold"),
    bg="blue",
    fg="white",
    width=1,
    bd=6,
    command=save_file
)
save_button.pack(side="left")




keywords_button = tk.Button(
    root,
    text="Kw",
    font=("Times", 8, "bold"),
    bg="yellow",
    fg="darkblue",
    width=1,
    bd=6,
    command=highlight_code
)
keywords_button.pack(side="left")


cut_button = tk.Button(
    root,
    text="P >",
    font=("Times", 8, "bold"),
    bg="lightgrey",
    fg="#000088",
    width=1,
    bd=6,
    command=run_python
)
cut_button.pack(side="left")


clear_button = tk.Button(
    root,
    text="Copy",
    font=("Times", 8, "bold"),
    bg="lightgreen",
    fg="#004400",
    width=1,
    bd=6,
    command=lambda: editor.event_generate("<<Copy>>")
)
clear_button.pack(side="left")

clear_button = tk.Button(
    root,
    text="Paste",
    font=("Times", 8, "bold"),
    bg="lightblue",
    fg="#000077",
    width=1,
    bd=6,
    command=lambda: editor.event_generate("<<Paste>>")
)
clear_button.pack(side="left")


# Reload whatever was in editor
def on_closing():
    with open("last_code.txt", "w") as f:
        f.write(editor.get(1.0, "end-1c"))


root.protocol("WM_DELETE_WINDOW", on_closing)

try:
    with open("last_code.txt", "r") as f:
        editor.insert(1.0, f.read())

except:
    pass


editor.focus_set()



editor.bind("<Return>", auto_indent)

root.mainloop()

