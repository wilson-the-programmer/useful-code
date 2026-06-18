

import io
import sys
import subprocess
import threading

import tkinter as tk

from tkinter import (
    filedialog,
    scrolledtext
)

import keyword
import re

unix_words = ["ls", "cat", "cp", "mv", "rm", "mkdir", "rmdir", "pwd", "cd", "echo", "touch", "clear", "whoami", "date", "cal", "grep", "find", "sort", "wc", "head", "tail", "less", "more", "gcc", "g++", "python", "python3", "flake8", "cpplint", "git", "make", "cmake", "ps", "top", "kill", "chmod", "chown"]


def undo_last():
    try:
        editor.edit_undo()
    except:
        pass


def redo_last():
    try:
        editor.edit_redo()
    except:
        pass


def list_files():
    current_window = root.focus_get()
    last_location = current_window.index("insert")
    line_content = current_window.get("insert linestart", "insert lineend")
    letter = line_content.strip().lower()
    process = subprocess.Popen(
        ["ls"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    output, _ = process.communicate()
    command_list = output.decode().splitlines()
    filtered_commands = [cmd for cmd in command_list if cmd.lower().startswith(letter)]
    if filtered_commands:
        current_window.delete("insert lineend", "end")
        for cmd in filtered_commands:
            current_window.insert("end", f"\n{cmd}")
    current_window.mark_set("insert", last_location)
    current_window.see("insert")


def open_file_from_cursor():
    current_window = root.focus_get()
    try:
        file = current_window.get("insert linestart", "insert lineend").strip()
        if not file:
            return
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
        current_window.delete("1.0", tk.END)
        current_window.insert(tk.END, content)
    except:
        pass



def auto_indent(event=None):
    detect_command()
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
    editor.tag_config("var", foreground="#8B5A2B")
    editor.tag_config("eq", foreground="#333333")
    editor.tag_config("num", foreground="blue")
    editor.tag_config("str", foreground="#E67300")
    editor.tag_config("call", foreground="green")


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
        

def copy_text():
    try:
        current_window = root.focus_get()
        text = current_window.get("sel.first", "sel.last")

        root.clipboard_clear()
        root.clipboard_append(text)
    except:
        pass


def cut_text():
    try:
        current_window = root.focus_get()
        text = current_window.get("sel.first", "sel.last")

        root.clipboard_clear()
        root.clipboard_append(text)

        current_window.delete("sel.first", "sel.last")
    except:
        pass


def paste_text():
    try:
        current_window = root.focus_get()

        try:
            current_window.delete("sel.first", "sel.last")
        except:
            pass

        current_window.insert("insert", root.clipboard_get())
    except:
        pass
        



def detect_command(event=None):
    current_window = root.focus_get()
    cmd = current_window.get("insert linestart", "insert lineend").strip()
    for c in unix_words:
        if c in cmd:
            unix_command()
            current_window.event_generate("return")


def unix_command():
    current_window = root.focus_get()
    command = current_window.get("insert linestart", "insert lineend").strip()

    def run_command():
        try:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                text=True
            )

            for line in process.stdout:
                current_window.insert("end", line)
                current_window.see("end")

            process.stdout.close()
            process.wait()

        except:
            pass

        current_window.see("end")

    current_window.see("insert")
    threading.Thread(target=run_command).start()


window_expanded = 0


def expand_window():
    global window_expanded

    try:
        window_expanded += 1

        if window_expanded > 1:
            window_expanded = 0

        if window_expanded == 1:
            editor.config(height=10)
            root.geometry("460x800+0+0")
        else:
            root.geometry("460x500+0+0")
            editor.config(height=5)

    except:
        pass
        

root = tk.Tk()
root.title("Python IDE")
root.config(bg="white")
root.geometry("460x500+0+0")
editor = tk.Text(
    root,
    wrap="word",
    font=("Courier New", 8),
    undo=True,
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
    side="top",
    pady=(65,0)
)



clear_button = tk.Button(
    root,
    text="Clr",
    font=("Times", 8, "bold"),
    bg="#250000",
    fg="red",
    width=1,
    bd=6,
    command=lambda: editor.delete(1.0, "end")
)
clear_button.place(x=0, y=2)


undo_button = tk.Button(
    root,
    text="Undo",
    font=("Times", 8, "bold"),
    bg="lightcyan",
    fg="darkblue",
    width=1,
    bd=6,
    command=undo_last
)
undo_button.place(x=77, y=2)

redo_button = tk.Button(
    root,
    text="Redo",
    font=("Times", 8, "bold"),
    bg="black",
    fg="cyan",
    width=1,
    bd=6,
    command=redo_last
)
redo_button.place(x=153, y=2)

files_button = tk.Button(
    root,
    text="ls *",
    font=("Times", 8, "bold"),
    bg="black",
    fg="lightgreen",
    width=1,
    bd=6,
    command=list_files
)
files_button.place(x=229, y=2)

view_button = tk.Button(
    root,
    text="View",
    font=("Times", 8, "bold"),
    bg="black",
    fg="lightgrey",
    width=1,
    bd=6,
    command=open_file_from_cursor
)
view_button.place(x=305, y=2)

expand_button = tk.Button(
    root,
    text="[]",
    font=("Times", 8, "bold"),
    bg="black",
    fg="orange",
    width=1,
    bd=6,
    command=expand_window
)
expand_button.place(x=382, y=2)

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
    command=copy_text
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
    command=paste_text
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

"""

Overview

This is a **Python code editor** built with `tkinter` (Python's GUI library). It's like a mini IDE with syntax highlighting and code execution features.

### Main Features:

1. **Syntax Highlighting** (`highlight_code` function)
   - Colors Python keywords red, variables dark red, numbers blue, strings green, etc.
   - Updates as you type

2. **Code Execution** (`run_python` function)
   - "P >" button runs the Python code in the editor
   - Shows output in a popup window

3. **Auto-Indentation** (`auto_indent` function)
   - Pressing Enter automatically indents to match the previous line
   - Helpful when writing functions/loops

4. **File Operations**
   - Open and save Python files
   - Remembers the last code you were working on (saves to `last_code.txt`)

5. **Utility Features**
   - Copy/Paste buttons
   - Quick expression evaluator (`eval_exp` - evaluates inline math)

### Layout
The editor has a text area and buttons at the bottom:
- **Open** - Load a file
- **Save** - Save your code
- **Kw** - Highlight keywords
- **P >** - Run Python code
- **Copy/Paste** - Clipboard operations


"""
