
import io
import sys
import re
import os
import random
import threading
import tempfile
import subprocess
import keyword
import builtins
import tkinter as tk
from tkinter import (
    filedialog,
    simpledialog,
    colorchooser,
    messagebox
)



mixed_words = [
    "append(",
    "clear(",
    "copy(",
    "count(",
    "del(",
    "extend(",
    "get(",
    "index(",
    "insert(",
    "items(",
    "join(",
    "keys(",
    "pop(",
    "remove(",
    "reverse(",
    "setdefault(",
    "sort(",
    "split(",
    "strip(",
    "update(",
    "values(",
    "replace(",
    "startswith(",
    "endswith(",
    "find(",
    "format(",
    "lower(",
    "upper(",
    "capitalize(",
    "title(",
    "False",
    "None",
    "True",
    "abs(",
    "any(",
    "ascii(",
    "assert",
    "async",
    "auto",
    "await",
    "bin(",
    "bool(",
    "break",
    "breakpoint(",
    "bytearray(",
    "bytes(",
    "callable(",
    "capitalize(",
    "case",
    "casefold(",
    "center(",
    "char",
    "chr(",
    "class",
    "classmethod(",
    "compile(",
    "complex(",
    "console",
    "const",
    "continue",
    "count(",
    "default",
    "delattr(",
    "dict(",
    "dir(",
    "divmod(",
    "do",
    "document",
    "double",
    "elif",
    "else",
    "encode(",
    "endswith(",
    "enum",
    "enumerate(",
    "eval(",
    "exec(",
    "exit(",
    "expandtabs(",
    "export",
    "extends",
    "extern",
    "false",
    "filter(",
    "finally",
    "find(",
    "float",
    "float(",
    "fmt",
    "for",
    "format(",
    "format_map(",
    "from",
    "frozenset(",
    "func",
    "function",
    "getattr(",
    "global",
    "globals(",
    "goto",
    "hasattr(",
    "hash(",
    "hex(",
    "if",
    "import",
    "include",
    "index(",
    "inline",
    "input(",
    "instanceof(",
    "int",
    "iostream",
    "isalnum(",
    "isalpha(",
    "isascii(",
    "isdecimal(",
    "isdigit(",
    "isidentifier(",
    "isinstance(",
    "islower(",
    "isnumeric(",
    "isprintable(",
    "isspace(",
    "issubclass(",
    "istitle(",
    "isupper(",
    "join(",
    "lambda",
    "list(",
    "ljust(",
    "locals(",
    "long",
    "lower(",
    "lstrip(",
    "main",
    "maketrans(",
    "map(",
    "match(",
    "matplot.pyplot",
    "max(",
    "memoryview(",
    "min(",
    "namespace",
    "next(",
    "nonlocal",
    "null",
    "numpy",
    "object(",
    "oct(",
    "open(",
    "ord(",
    "partition(",
    "pass",
    "pow(",
    "print(",
    "prompt_toolkit",
    "property(",
    "quit(",
    "raise",
    "random",
    "range(",
    "register",
    "removeprefix(",
    "removesuffix(",
    "replace(",
    "repr(",
    "restrict",
    "return",
    "reversed(",
    "rfind(",
    "rindex(",
    "rjust(",
    "round(",
    "rpartition(",
    "rsplit(",
    "rstrip(",
    "scipy",
    "set(",
    "setattr(",
    "short",
    "signed",
    "sizeof",
    "slice(",
    "sorted(",
    "split(",
    "splitlines(",
    "startswith(",
    "static",
    "staticmethod(",
    "str(",
    "strip(",
    "struct",
    "sum(",
    "super(",
    "swapcase(",
    "switch",
    "this",
    "title(",
    "tkinter",
    "translate(",
    "true",
    "tuple(",
    "typedef",
    "typeof",
    "undefined",
    "union",
    "unsigned",
    "upper(",
    "vars(",
    "void",
    "volatile",
    "while",
    "window",
    "with",
    "yield",
    "zfill(",

]

unix_words = [
    "alias",
    "awk",
    "base64",
    "basename",
    "bash",
    "break",
    "builtin",
    "busybox",
    "bzcat",
    "cat",
    "chgrp",
    "chmod",
    "chown",
    "cksum",
    "clear",
    "cmp",
    "command",
    "continue",
    "cut",
    "date",
    "diff",
    "dirname",
    "dos2unix",
    "echo",
    "egrep",
    "env",
    "eval",
    "exec",
    "expand",
    "expr",
    "false",
    "fgrep",
    "find",
    "getopts",
    "grep",
    "gunzip",
    "gzip",
    "hash",
    "head",
    "help",
    "history",
    "jobs",
    "kill",
    "killall",
    "local",
    "logout",
    "ls",
    "lsof",
    "lzcat",
    "md5sum",
    "mkdir",
    "mkfifo",
    "more",
    "mount",
    "nohup",
    "paste",
    "patch",
    "pkill",
    "printenv",
    "printf",
    "pwd",
    "read",
    "readlink",
    "readonly",
    "realpath",
    "return",
    "rmdir",
    "sed",
    "set",
    "shift",
    "sleep",
    "sort",
    "source",
    "split",
    "stat",
    "stty",
    "sum",
    "sync",
    "tac",
    "tail",
    "tar",
    "tee",
    "test",
    "time",
    "timeout",
    "touch",
    "trap",
    "true",
    "truncate",
    "tty",
    "type",
    "ulimit",
    "umask",
    "unalias",
    "uname",
    "unexpand",
    "uniq",
    "unix2dos",
    "unlink",
    "unxz",
    "unzip",
    "unset",
    "usleep",
    "wait",
    "which",
    "xargs",
    "xzcat",
    "zcat"
]


dir_list = []

my_variables = []

home_files = os.listdir(".")

all_words = sorted(set(keyword.kwlist + dir(builtins) + mixed_words + unix_words + dir_list))




def update_variables(event=None):
    global my_var

    cursor_line = int(editor.index("insert").split(".")[0])
    start_line = max(1, cursor_line - 10)
    end_line = cursor_line + 10

    text = editor.get(f"{start_line}.0", f"{end_line}.end")

    for match in re.finditer(r"(?<![=!<>])\b([a-zA-Z_]\w*)\s+=\s*(?!=)", text):
        variable = match.group(1)

        if variable not in my_variables:
            my_variables.append(variable)

        if len(my_variables) >= 25:
            my_variables.pop(0)


def update_dir_list(event=None):
    global dir_list

    lines_checked = editor.get("1.0", "8.end")
    libraries = []

    for line in lines_checked.splitlines():
        match = re.match(r"\s*import\s+([\w.]+)", line)

        if match:
            libraries.append(match.group(1))

        if len(libraries) == 4:
            break

    for library in libraries:
        try:
            module = __import__(library, fromlist=["*"])

            for name in sorted(dir(module)):
                if not name.startswith("_") and callable(getattr(module, name, None)):
                    dir_list.append(f"{name}(")

                    if len(dir_list) > 100:
                        dir_list.pop(-1)

                    if len(dir_list) >= 25:
                        break

        except ImportError:
            continue



def quick_hex(r, g, b):
	return f"#{r:02x}{g:02x}{b:02x}"
	
def insert_spaces():
	editor.insert("insert", "    ")




def run_python():
    current_window = root.focus_get()
    code = current_window.get("1.0", tk.END)

    output = io.StringIO()
    sys.stdout = output

    try:
        exec(code)

    except Exception as e:
        output.write(f"{type(e).__name__}: {e}")

    finally:
        sys.stdout = sys.__stdout__

        if current_window == editor:
            result_window.delete(1.0, "end")
            result_window.insert(1.0, output.getvalue())
        else:
            editor.delete(1.0, "end")
            editor.insert(1.0, output.getvalue())

last_file_opened = ""


def open_file():
    global last_file_opened
    current_window = root.focus_get()

    file_path = filedialog.askopenfilename(
        filetypes=[
            ("Python", "*.py*"),
            ("C", "*.c"),
            ("Text", "*.txt"),
        ]
    )

    if file_path:
        last_file_opened = file_path.split("/")[-1]
        with open(file_path, "r") as file:
            content = file.read()
            current_window.delete("1.0", tk.END)
            current_window.insert(tk.INSERT, f"\n{content}")
            result_window.insert(1.0, last_file_opened)


def open_file_from_cursor():
    global last_file_opened
    current_window = root.focus_get()
    try:
        file = current_window.get("insert linestart", "insert lineend").strip()
        last_file_opened = file.split("/")[-1]
        if not file:
            return
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
        current_window.delete("1.0", tk.END)
        current_window.insert(tk.END, content)
    except:
        pass
        

def save_file():
    current_window = root.focus_get()
    filename = filedialog.asksaveasfilename(defaultextension=".txt")

    if filename:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(current_window.get("1.0", "end-1c"))


def save_last_opened():
    current_window = root.focus_get()
    if last_file_opened:
    	with open(last_file_opened, "w", encoding="utf-8") as file:
    		file.write(current_window.get("1.0", "end-1c"))
    		status_window.insert(0, f"File: {last_file_opened} Saved")
    		root.after(2000, lambda: status_window.delete(0, "end"))
    		
    else:
    	save_file()


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
        

def smart_tab(event=None):
    current_widget = root.focus_get()
    char_left = current_widget.get("insert-1c", "insert")
    text = current_widget.get("insert linestart", "insert lineend").strip()
    try:
        if text:
            last_word = text.split()[-1]
            last_char = text.split()[-1][-1]
        for i in [":", "("]:
            if i == char_left:
                root.after(100, lambda: current_widget.insert(tk.INSERT, "    "))
                
    except:
        pass

def color_word(event=None):
    start = "1.0"
    end = editor.index("1.0 wordend")

    color = "#{:02x}{:02x}{:02x}".format(
        random.randint(80, 255),
        random.randint(80, 255),
        random.randint(80, 255)
    )

    editor.tag_add("random_color", start, end)
    editor.tag_config("random_color", foreground=color)
    
    result_window.delete(1.0, "1.end")
    result_window.insert(1.0, color)
    


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


def copy_text():
    current_widget = root.focus_get()
    if hasattr(current_widget, "selection_get"):
        selected_text = current_widget.selection_get()
        root.clipboard_clear()
        root.clipboard_append(selected_text)


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
     
def auto_indent(event=None):
    detect_command()
    smart_tab()
    current_window = root.focus_get()
    current_line = int(current_window.index("insert").split(".")[0])
    start_of_line = f"{current_line}.0"
    text_contents = current_window.get(start_of_line, start_of_line + " lineend")
    indentation = text_contents[: len(text_contents) - len(text_contents.lstrip())]
    if indentation and current_line == int(
        current_window.index("insert").split(".")[0]
    ):
        current_window.insert("insert", "\n" + indentation)
        current_window.see("insert")
        return "break"
    else:
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
                command, shell=True, stdout=subprocess.PIPE, text=True
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
    


def goto_line_selected(event=None):

    try:
        current_window = root.focus_get()

        line_text = current_window.get("insert linestart", "insert lineend")

        match = re.search(r"\d+", line_text)

        if not match:
            return

        line = int(match.group())

        if line < 1:
            return

        editor.mark_set("insert", f"{line}.0")
        editor.see(f"{line}.0")

        editor.tag_add("current_line", f"{line}.0", f"{line}.0 lineend")

        editor.focus_set()
      

    except:
        pass


def run_c():
    current_window = root.focus_get()

    def task():
        try:
            code = current_window.get(1.0, "end")
            f = tempfile.NamedTemporaryFile(
                delete=False, suffix=".c", mode="w", encoding="utf-8"
            )

            f.write(code)
            f.close()

            exe = f.name + ".out"

            try:
                c = subprocess.run(
                    ["gcc", f.name, "-o", exe], capture_output=True, text=True
                )

                if c.returncode != 0:
                    if current_window == editor:
                        result_window.delete(1.0, "end")
                        result_window.insert(1.0, c.stderr)
                        return
                    else:
                        editor.delete(1.0, "end")
                        editor.insert(1.0, c.stderr)
                        return

                r = subprocess.run([exe], capture_output=True, text=True)

                result_window.delete(1.0, "end")
                result_window.insert(1.0, r.stdout + r.stderr)

            finally:
                if os.path.exists(f.name):
                    os.unlink(f.name)

                if os.path.exists(exe):
                    os.unlink(exe)

        except Exception as e:

            if current_window == editor:
                result_window.delete(1.0, "end")
                result_window.insert(1.0, e)
            else:
                editor.delete(1.0, "end")
                editor.insert(1.0, e)

    threading.Thread(target=task, daemon=True).start()



def clear_screen():
	current_widget = root.focus_get()
	confirm = messagebox.askyesno("Are You Sure", "Clear All ?")
	if confirm:
		current_widget.delete(1.0, "end")


def swap_windows():
    confirm = messagebox.askyesno("Swap Top & Bottom", "Switch?")
    if confirm:
        editor_text = editor.get("1.0", "end-1c")
        result_text = result_window.get("1.0", "end-1c")

        editor.delete("1.0", "end")
        result_window.delete("1.0", "end")

        editor.insert("1.0", result_text)
        result_window.insert("1.0", editor_text)



python_words = set(keyword.kwlist + all_words)

func_words = [
    "abs(",
    "append(",
    "capitalize(",
    "clear(",
    "copy(",
    "count(",
    "del(",
    "dict(",
    "endswith(",
    "enumerate(",
    "extend(",
    "find(",
    "float(",
    "format(",
    "get(",
    "index(",
    "input(",
    "insert(",
    "int(",
    "items(",
    "join(",
    "keys(",
    "len(",
    "list(",
    "lower(",
    "max(",
    "min(",
    "open(",
    "pop(",
    "print(",
    "range(",
    "remove(",
    "replace(",
    "reverse(",
    "round(",
    "set(",
    "setdefault(",
    "sorted(",
    "sort(",
    "split(",
    "startswith(",
    "str(",
    "strip(",
    "sum(",
    "title(",
    "tuple(",
    "type(",
    "update(",
    "upper(",
    "values("
]

def highlight_words(event=None):
    
    kw_color = "#ef9f93"
    func_color = "cyan"
    
    
    start = editor.index("insert - 10 lines linestart")
    end = editor.index("insert + 10 lines linestart")
    text = editor.get(start, end)

    def scan():

        results = []

        for word, tag in [(w, kw_color) for w in python_words] + [(w, func_color) for w in func_words]:
            for match in re.finditer(r"\b" + re.escape(word) + r"\b", text):
                results.append((match.start(), match.end(), tag))

        def apply():
            editor.tag_remove(kw_color, start, end)
            editor.tag_remove(func_color, start, end)

            for first, last, tag in results:
                editor.tag_add(
                    tag,
                    f"{start} + {first} chars",
                    f"{start} + {last} chars"
                )

            editor.tag_config(kw_color, foreground=kw_color)
            editor.tag_config(func_color, foreground=func_color)

        editor.after(0, apply)

    threading.Thread(target=scan, daemon=True).start()


def highlight_variables(event=None):
    color = "#f18e93"
    cursor_line = int(editor.index("insert").split(".")[0])
    start_line = max(1, cursor_line - 10)
    end_line = cursor_line + 10

    editor.tag_remove(color, "1.0", "end")
    text = editor.get(f"{start_line}.0", f"{end_line}.end")

    for match in re.finditer(r"\b[a-zA-Z_]\w*(?=\s*=)", text):
        start = f"{start_line}.0 + {match.start()} chars"
        end = f"{start_line}.0 + {match.end()} chars"
        editor.tag_add(color, start, end)

    editor.tag_config(color, foreground=color)


def highlight_numbers(event=None):
    color = "#b8b371"
    cursor_line = int(editor.index("insert").split(".")[0])
    start_line = max(1, cursor_line - 10)
    end_line = cursor_line + 10

    editor.tag_remove(color, "1.0", "end")
    text = editor.get(f"{start_line}.0", f"{end_line}.end")

    for match in re.finditer(r"\b\d+\.?\d*\b", text):
        start = f"{start_line}.0 + {match.start()} chars"
        end = f"{start_line}.0 + {match.end()} chars"
        editor.tag_add(color, start, end)

    editor.tag_config(color, foreground=color)
    

def highlight_symbols(event=None):
    color = "#8cbef3"
    cursor_line = int(editor.index("insert").split(".")[0])
    start_line = max(1, cursor_line - 10)
    end_line = cursor_line + 10

    editor.tag_remove(color, "1.0", "end")
    text = editor.get(f"{start_line}.0", f"{end_line}.end")

    for match in re.finditer(r"[@=$_&\-+()/\*:;!?%{}\\\[\]<>^,.✓]", text):
        start = f"{start_line}.0 + {match.start()} chars"
        end = f"{start_line}.0 + {match.end()} chars"
        editor.tag_add(color, start, end)

    editor.tag_config(color, foreground=color)


def highlight_strings(event=None):
    color = "orange"
    cursor_line = int(editor.index("insert").split(".")[0])
    start_line = max(1, cursor_line - 10)
    end_line = cursor_line + 10

    editor.tag_remove(color, "1.0", "end")
    text = editor.get(f"{start_line}.0", f"{end_line}.end")

    for match in re.finditer(r"""(['"]).*?\1|(""" + r"""'''.*?'''|""".replace('"', '\\"') + r"""\"\"\".*?\"\"\")""", text, re.DOTALL):
        start = f"{start_line}.0 + {match.start()} chars"
        end = f"{start_line}.0 + {match.end()} chars"
        editor.tag_add(color, start, end)

    editor.tag_config(color, foreground=color)


def update_cursor_position(event=None):
    
    line, column = editor.index("insert").split(".")
    status_window.delete(0, "end")
    status_window.insert(0, f"{line}, {column}")
    



def show_code_map(event=None):
    result_window.delete("1.0", "end")
    code = editor.get("1.0", "end")
    functions = {}
    variables = {}

    for line_number, line in enumerate(code.splitlines(), 1):
        function = re.match(r"\s*def\s+(\w+)\s*\(", line)
        if function:
            functions[function.group(1) + "()"] = line_number

        assignment = re.match(r"\s*([a-zA-Z_]\w*)\s*=", line)
        if assignment:
            name = assignment.group(1)
            if name not in {
                "bg", "fg", "font", "text", "width", "height",
                "bd", "padx", "pady", "relief", "command",
                "root", "editor", "label"
            }:
                variables[name] = line_number

    result_window.insert("end", "Functions:\n\n")
    for name in sorted(functions):
        result_window.insert("end", f"{name}, {functions[name]}\n")

    result_window.insert("end", "\nVariables:\n\n")
    for name in sorted(variables):
        result_window.insert("end", f"{name}, {variables[name]}\n")
        
        
        
widget_expanded = False

def expand_widget():
    global widget_expanded
    widget_expanded = not widget_expanded

    if widget_expanded:
        root.geometry("700x1280+0+0")
    else:
        root.geometry("690x760+0+0")
   
   
def quick_uni():
    current_widget = result_window
    start = simpledialog.askinteger("Enter Start Value", "Start: ")
    end = simpledialog.askinteger("Enter End Value", "End ")
    current_widget.delete(1.0, "end")
    for i in range(start, end):
        
        current_widget.insert(1.0, f"\nchr({i}) = {chr(i)}")
        
        


   
   
#---------------

theme_bg = "blue",
theme_fg = "white"

root = tk.Tk()

root.geometry("690x760")

root.config(bg="darkcyan")


editor = tk.Text(
    root,
    wrap="word",
    padx=10,
    pady=10,
    undo=True,
    height=10,
    insertwidth=4,
    insertbackground="lightgrey",
    bd=1,
    font=("Courier New", 8),
    bg="black",
    fg="lightgrey",
)
editor.pack(expand=True, fill="both", side="top", pady=(0, 0))


status_window = tk.Entry(
    root,
    insertbackground="cyan",
    insertwidth=5,
    bd=5,
    bg="#331100",
    fg="red",
    font=("Courier New", 9),
)
status_window.pack(side="top", fill="x")

result_window = tk.Text(
    root,
    wrap="word",
    padx=10,
    pady=10,
    height=3,
    insertbackground="cyan",
    insertwidth=5,
    bd=2,
    bg="#255157",
    fg="white",
    font=("Courier New", 8),
)
result_window.pack(expand=True, fill="both", side="top")

menu = tk.Menu(
    root,
    bd=4,
    font=("Courier New", 11),
    bg = theme_bg,
    fg = theme_fg
)




root.config(menu=menu)


file_menu = tk.Menu(menu, tearoff=0, font=("Courier New", 11))

menu.add_cascade(label="File", menu=file_menu)


file_menu.add_command(label="Open", command=open_file)


file_menu.add_command(label="Save", command=save_file)

file_menu.add_command(label="Expand Screen []", command=expand_widget)

file_menu.add_command(label="Swap Top & Bottom ⇆", command=swap_windows)


file_menu.add_command(label="Code Map", command=show_code_map)

file_menu.add_command(label="Unicodes", command=quick_uni)



file_menu.add_command(label="See Dir List", command=lambda: (result_window.delete(1.0, "end"), result_window.insert(1.0, dir_list)))




edit_menu = tk.Menu(menu, tearoff=0, font=("Courier New", 11))

menu.add_cascade(label="Edit", menu=edit_menu)


edit_menu.add_command(label="Cut ✂", command=cut_text)

edit_menu.add_command(label="Copy ⎘", command=copy_text)

edit_menu.add_command(label="Paste ⎙", command=paste_text)


edit_menu.add_command(label="Color First Word", command=color_word)



edit_menu.add_command(label="Undo ↶", command=undo_last)

edit_menu.add_command(label="Redo ↷", command=redo_last)

edit_menu.add_command(label="Clear Screen", command=clear_screen)


files_button = tk.Button(
    root,
    command=list_files,
    text="ls *",
    width=1,
    bd=4,
    bg=theme_bg,
    fg=theme_fg,
    font=("Times", 10),
)

files_button.pack(side="left")


view_button = tk.Button(
    root,
    command=open_file_from_cursor,
    text="View",
    width=1,
    bd=4,
    bg=theme_bg,
    fg=theme_fg,
    font=("Times", 10),
)

view_button.pack(side="left")




open_button = tk.Button(
    root,
    command=undo_last,
    text="↶",
    width=1,
    bd=4,
    bg=theme_bg,
    fg=theme_fg,
    font=("Times", 10, "bold"),
)

open_button.pack(side="left")



save_button = tk.Button(
    root,
    command=save_last_opened,
    text="Save",
    width=1,
    bd=4,
    bg=theme_bg,
    fg=theme_fg,
    font=("Times", 10),
)

save_button.pack(side="left")




files_button = tk.Button(
    root,
    command=run_c,
    text="C >",
    width=1,
    bd=4,
    bg="black",
    fg="gold",
    font=("Times", 10, "bold"),
)

files_button.pack(side="left")





python_button = tk.Button(
    root,
    command=run_python,
    text="P >",
    width=1,
    bd=4,
    bg="black",
    fg="darkorange",
    font=("Times", 10, "bold"),
)

python_button.pack(side="left")


expand_button = tk.Button(
    root,
    command=expand_widget,
    text="[]",
    width=1,
    bd=4,
    bg=theme_bg,
    fg=theme_fg,
    font=("Times", 10),
)

expand_button.pack(side="left")







popup = None
suggestions = None
current_word_start = None


def close_popup():
    global popup, suggestions

    if popup is not None:
        popup.destroy()
        popup = None
        suggestions = None


def select_word(event):
    global current_word_start

    if popup is None or suggestions is None:
        return

    selected = suggestions.curselection()

    if not selected:
        return

    selected_word = suggestions.get(selected[0])

    if current_word_start is not None:
        editor.delete(current_word_start, "insert")
        editor.insert("insert", selected_word)

    close_popup()
    editor.focus_set()


def auto_suggest(event=None):
    highlight_words()
    highlight_variables()
    highlight_numbers()
    highlight_strings()
    highlight_symbols()
    update_dir_list()
    update_variables()
    update_cursor_position()
    
    global popup, suggestions, current_word_start

    if event and event.keysym in ("Escape", "Return", "Up", "Down", "Tab"):
        if event.keysym == "Escape":
            close_popup()
        return

    line_start = editor.index("insert linestart")
    cursor_position = editor.index("insert")
    line = editor.get(line_start, cursor_position)

    current_word = ""
    for character in reversed(line):
        if character.isalnum() or character == "_":
            current_word = character + current_word
        else:
            break

    if not current_word:
        close_popup()
        return

    current_word_start = f"{cursor_position} - {len(current_word)} chars"

    matches = [
        item for item in all_words + dir_list + my_variables
        if item.lower().startswith(current_word.lower())
        and item.lower() != current_word.lower()
    ]

    if not matches:
        close_popup()
        return

    if popup is None:
        popup = tk.Toplevel(root)
        popup.overrideredirect(True)

        suggestions = tk.Listbox(
            popup,
            width=20,
            height=15,
            bg="#204157",
            fg="white",
            font=("Courier New", 9),
            exportselection=False
        )
        suggestions.pack()
        suggestions.bind("<ButtonRelease-1>", select_word)

    suggestions.delete(0, tk.END)

    for item in matches:
        suggestions.insert(tk.END, item)

    suggestions.selection_clear(0, tk.END)
    suggestions.selection_set(0)
    suggestions.activate(0)

    root.update_idletasks()

    cursor_box = editor.bbox("insert")

    if cursor_box:
        cursor_x, cursor_y, _, cursor_height = cursor_box
        x = editor.winfo_rootx() + cursor_x
        y = editor.winfo_rooty() + cursor_y + cursor_height

        popup.geometry(f"+{x}+{y}")
        popup.lift()
        




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


#current_page_words = sorted(set(editor.get("1.0", "end").split()))


editor.bind("<KeyRelease>", auto_suggest)

editor.bind("<Return>", auto_indent)

editor.bind("<Button-1>", lambda x: (highlight_words(), update_cursor_position()))


result_window.bind("<Return>", auto_indent)


result_window.bind("<Button-1>", goto_line_selected)

root.mainloop()
