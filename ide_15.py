import tkinter as tk
from tkinter import (
    scrolledtext,
    filedialog
)

import math
import re
import os
import io
import subprocess
import sys
import keyword
import threading
import tempfile

from pypinyin import pinyin, Style
from deep_translator import GoogleTranslator


from transliterate import translit


def capitalize_left():
    cursor = editor.index("insert")

    if cursor == "1.0":
        return

    left_pos = editor.index(f"{cursor}-1c")

    ch = editor.get(left_pos, cursor)

    if ch.strip() == "":
        return

    editor.delete(left_pos, cursor)
    editor.insert(left_pos, ch.upper())
    

def mandarin_translator():
    current_window = root.focus_get()
    text = current_window.get("insert linestart", "insert lineend").strip()

    if not text:
        return

    try:
        chinese = GoogleTranslator(source="auto", target="zh-CN").translate(text)

        pinyin_text = " ".join(item[0] for item in pinyin(chinese, style=Style.TONE))
        

        current_window.insert("insert", f"\n\n{chinese}\n" f"{pinyin_text}\n\n")
        current_window.see("insert")

    except:
        pass
        

window_expanded = 0


def expand_window():
    global window_expanded

    try:
        window_expanded += 1

        if window_expanded > 1:
            window_expanded = 0

        if window_expanded == 1:
            editor.config(height=10)
        else:
            editor.config(height=5)

    except:
        pass



def compile_exe_c():
    def task():
        try:
            code = editor.get("1.0", "end-1c")

            f = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".c",
                mode="w",
                encoding="utf-8"
            )

            f.write(code)
            f.close()

            exe = f.name + ".out"

            try:
                c = subprocess.run(["gcc", f.name, "-o", exe], capture_output=True, text=True)

                if c.returncode != 0:
                    show_output(c.stderr)
                    return

                r = subprocess.run([exe], capture_output=True, text=True)

                show_output(r.stdout + r.stderr)

            finally:
                if os.path.exists(f.name):
                    os.unlink(f.name)

                if os.path.exists(exe):
                    os.unlink(exe)

        except Exception as e:
            show_output(str(e))

    threading.Thread(target=task, daemon=True).start()    



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

        show_output(output.getvalue())
        



def open_file():
    current_widget = root.focus_get()

    file_path = filedialog.askopenfilename(
        filetypes=[
            ("Python", "*.py*"),
            ("C", "*.c"),
            ("C++", "*.cpp"),
            ("Text", "*.txt"),
        ]
    )

    if file_path:
        with open(file_path, "r") as file:
            content = file.read()
            current_widget.delete("1.0", tk.END)
            current_widget.insert(tk.INSERT, f"\n{content}")


def save_file():
    current_window = root.focus_get()
    filename = filedialog.asksaveasfilename(
        defaultextension=".txt"
    )

    if filename:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(current_window.get("1.0", "end-1c"))



def show_output(result):
    output_window = tk.Toplevel(root)
    output_window.geometry("460x500+0+0")
    

    result_text = tk.Text(
        output_window,
        wrap="word",
        font=("Courier New", 8),
        height=5,
        bg="white",
        fg="black",
        padx=8,
        pady=8,
        bd=2,
        insertbackground="red",
        insertwidth=6
    )
    result_text.pack(
        fill="both",
        expand=True
    )

    result_text.insert("1.0", result)
        
    exit_button = tk.Button(
        output_window,
        text="Exit",
        command=lambda: output_window.destroy(),
        font=("Courier New", 8),
        bd=5,
        width=2,
        bg="lightgrey",
        fg="darkblue" 
            
    )
        
    exit_button.pack(side="left")


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
    editor.tag_config("var", foreground="#8B5A2B")
    editor.tag_config("eq", foreground="#333333")
    editor.tag_config("num", foreground="blue")
    editor.tag_config("str", foreground="#E67300")
    editor.tag_config("call", foreground="green")

root = tk.Tk()
root.geometry("460x800")
root.config(bg="white")


editor = tk.Text(
    root,
    height=5,
    font=("Courier New", 8),
    bg="white",
    fg="black",
    bd=5,
    padx=8,
    pady=8,
    insertbackground="#000044",
    insertwidth=5,
  
)
editor.pack(fill="x", padx=6, pady=6)

safe = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "sqrt": math.sqrt,
    "log": math.log,
    "log10": math.log10,
    "exp": math.exp,
    "pi": math.pi,
    "e": math.e,
    "abs": abs
}

def insert(v):
    editor.insert(tk.INSERT, v)
    editor.focus_set()

def clear():
    editor.delete("1.0", tk.END)



def solve():
    try:
        expr = editor.get("insert linestart", "insert lineend").strip()
        result = eval(expr, {"__builtins__": {}}, safe)
        
        editor.insert("insert", f" = {str(result)}")

        editor.focus_set()
        editor.see("insert")
    except:
        editor.see("insert")
        editor.insert("insert", " = Error")
        editor.event_generate("<Return>")

frame = tk.Frame(root)
frame.pack(expand=True, fill="both")

buttons = [
    "C", "(", ")", "*", "←", "KW",
    "7", "8", "9", "/", "中国人", "[]",
    "4", "5", "6", "+", "Open", "Save",
    "1", "2", "3", "-", "C >", "P >",
    "0", ".", "=", "A↑", "⌫", "⏎"
]

def on_click(b):
    if b == "C":
        clear()
    elif b == "=":
        solve()
    elif b == "ln":
        insert("log(")
    elif b == "A↑":
    	capitalize_left()
    elif b == "[]":
    	expand_window()
    elif b == "←":
    	editor.event_generate("<Left>")
    elif b == "→":
    	editor.event_generate("<Right>")
    elif b == "⌫":
    	editor.event_generate("<BackSpace>")
    elif b == "⏎":
    	editor.event_generate("<Return>")
    elif b == "KW":
    	highlight_code()
    elif b == "Open":
    	open_file()
    elif b == "Save":
    	save_file()
    elif b == "P >":
    	run_python()
    elif b == "C >":
    	compile_exe_c()
    	
    
    else:
        insert(b)
        editor.see("insert")

rows = 5
cols = 6

for i in range(rows):
    frame.rowconfigure(i, weight=1)

for j in range(cols):
    frame.columnconfigure(j, weight=1)

index = 0
for r in range(rows):
    for c in range(cols):
        if index >= len(buttons):
            break

        b = buttons[index]

        tk.Button(
            frame,
            text=b,
            bg="lightyellow",
            fg="blue",
            font=("Courier New", 8),
            command=lambda v=b: on_click(v)
        ).grid(
            row=r,
            column=c,
            sticky="nsew",
            padx=1,
            pady=1,
           
        )

        index += 1

keyboard = tk.Frame(root)
keyboard.pack(fill="both", expand=True, padx=4, pady=4)

keys = [
    list("qwertyuiop"),
    list("asdfghjkl⌫"),
    list("zxcvbnm  ⏎"),
    list('.,=()[]{}"'),
    list("\/|_^%#@$&")
    
]

def virtual_key(k):
    if k == " ":
        insert(" ")
    elif k == "←":
        editor.event_generate("<Left>")
    elif k == "⏎":
    	editor.event_generate("<Return>")

    elif k == "⌫":
    	editor.event_generate("<BackSpace>")
    	
    else:
        insert(k)
        editor.see("insert")

for r, row in enumerate(keys):
    for c, key in enumerate(row):
        tk.Button(
            keyboard,
            text=key,
            font=("Courier New", 10),
            bg="black",
            fg="lightgrey",
            
            command=lambda v=key: virtual_key(v)
        ).grid(
            row=r,
            column=c,
            sticky="nsew"
            
        )

for r in range(len(keys)):
    keyboard.rowconfigure(r, weight=1)

for c in range(10):
    keyboard.columnconfigure(c, weight=1)
    
    
    
    
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



root.mainloop()
