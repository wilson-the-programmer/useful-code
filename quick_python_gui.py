
import io
import sys
import re
import os
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



mixed_keywords = [
    "#include",
    "<iostream>",
    "Boolean(",
    "False",
    "None",
    "Println(",
    "Symbol",
    "True",
    "abs(",
    "any(",
    "ascii(",
    "assert",
    "async",
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
    "chr(",
    "classmethod(",
    "class",
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
    "document",
    "elif",
    "else",
    "encode(",
    "endswith(",
    "enumerate(",
    "eval(",
    "exec(",
    "exit(",
    "expandtabs(",
    "export",
    "extends",
    "false",
    "filter(",
    "finally",
    "find(",
    "float(",
    "fmt",
    "format(",
    "format_map(",
    "from",
    "frozenset(",
    "func",
    "function",
    "getattr(",
    "globals(",
    "global",
    "hash(",
    "hasattr(",
    "hex(",
    "import",
    "index(",
    "input(",
    "instanceof(",
    "isinstance(",
    "issubclass(",
    "isalnum(",
    "isalpha(",
    "isascii(",
    "isdecimal(",
    "isdigit(",
    "isidentifier(",
    "islower(",
    "isnumeric(",
    "isprintable(",
    "isspace(",
    "istitle(",
    "isupper(",
    "join(",
    "lambda",
    "list(",
    "ljust(",
    "locals(",
    "lower(",
    "lstrip(",
    "main",
    "maketrans(",
    "map(",
    "match(",
    "max(",
    "memoryview(",
    "min(",
    "namespace",
    "next(",
    "nonlocal",
    "null",
    "object(",
    "oct(",
    "open(",
    "ord(",
    "partition(",
    "pass",
    "pow(",
    "print(",
    "property(",
    "quit(",
    "random",
    "raise",
    "range(",
    "repr(",
    "removeprefix(",
    "removesuffix(",
    "replace(",
    "return",
    "reversed(",
    "rfind(",
    "rindex(",
    "rjust(",
    "round(",
    "rpartition(",
    "rsplit(",
    "rstrip(",
    "set(",
    "setattr(",
    "slice(",
    "sorted(",
    "split(",
    "splitlines(",
    "startswith(",
    "static",
    "staticmethod(",
    "str(",
    "strip(",
    "sum(",
    "super(",
    "swapcase(",
    "switch",
    "this",
    "title(",
    "translate(",
    "true",
    "tuple(",
    "typeof",
    "undefined",
    "upper(",
    "vars(",
    "while",
    "window",
    "with",
    "yield",
    "zfill(",
    "matplot.pyplot",
    "numpy",
    "prompt_toolkit",
    "scipy",
    "tkinter",
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

def quick_hex(r, g, b):
	return f"#{r:02x}{g:02x}{b:02x}"
	
def insert_spaces():
	editor.insert("insert", "    ")

home_files = os.listdir(".")



all_words = sorted(set(keyword.kwlist + dir(builtins) + mixed_keywords + unix_words))


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
    		result_window.insert(1.0, f"File: {last_file_opened} Saved")
    		root.after(2000, lambda: result_window.delete(1.0, "1.end"))
    		
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
     
def auto_indent(event=None):
    detect_command()
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
	confirm = messagebox.askyesno("Are You Sure", "Clear All ?")
	if confirm:
		editor.delete(1.0, "end")




python_words = set(keyword.kwlist)
green_words = [
    "print",
    "input",
    "len",
    "range",
    "str",
    "int",
    "float",
    "list",
    "dict",
    "set",
    "tuple",
    "type",
    "open",
    "sum",
    "min",
    "max",
    "abs",
    "round",
    "sorted",
    "enumerate"
]

def highlight_words(event=None):
    start = editor.index("insert - 3 lines linestart")
    end = editor.index("insert + 4 lines linestart")
    text = editor.get(start, end)

    def scan():
        import re

        results = []

        for word, tag in [(w, "orange") for w in python_words] + [(w, "gold") for w in green_words]:
            for match in re.finditer(r"\b" + re.escape(word) + r"\b", text):
                results.append((match.start(), match.end(), tag))

        def apply():
            editor.tag_remove("orange", start, end)
            editor.tag_remove("gold", start, end)

            for first, last, tag in results:
                editor.tag_add(
                    tag,
                    f"{start} + {first} chars",
                    f"{start} + {last} chars"
                )

            editor.tag_config("orange", foreground="orange")
            editor.tag_config("gold", foreground="gold")

        editor.after(0, apply)

    threading.Thread(target=scan, daemon=True).start()


root = tk.Tk()

root.geometry("690x760")


editor = tk.Text(
    root,
    wrap="word",
    padx=10,
    pady=10,
    undo=True,
    height=8,
    insertwidth=4,
    insertbackground="cyan",
    bd=1,
    font=("Courier New", 8),
    bg="black",
    fg="lightgrey",
)
editor.pack(expand=True, fill="both", side="top")

result_window = tk.Text(
    root,
    wrap="word",
    padx=10,
    pady=10,
    height=4,
    insertbackground="red",
    insertwidth=5,
    bd=2,
    bg="lightyellow",
    fg="blue",
    font=("Courier New", 9),
)
result_window.pack(expand=True, fill="both", side="top")

menu = tk.Menu(
    root,
    bd=4,
    font=("Courier New", 11),
    bg = "lightcyan",
    fg = "darkblue"
)



root.config(menu=menu)


file_menu = tk.Menu(menu, tearoff=0, font=("Courier New", 11))

menu.add_cascade(label="File", menu=file_menu)


file_menu.add_command(label="Open", command=open_file)


file_menu.add_command(label="Save", command=save_file)


files_button = tk.Button(
    root,
    command=list_files,
    text="ls *",
    width=1,
    bd=6,
    bg="lightblue",
    fg="darkblue",
    font=("Times", 10),
)

files_button.pack(side="left")


view_button = tk.Button(
    root,
    command=open_file_from_cursor,
    text="View",
    width=1,
    bd=6,
    bg="lightcyan",
    fg="darkblue",
    font=("Times", 10),
)

view_button.pack(side="left")




open_button = tk.Button(
    root,
    command=undo_last,
    text="Undo",
    width=1,
    bd=6,
    bg="lightyellow",
    fg="blue",
    font=("Times", 10),
)

open_button.pack(side="left")



save_button = tk.Button(
    root,
    command=save_last_opened,
    text="Save",
    width=1,
    bd=6,
    bg="lightgreen",
    fg="darkgreen",
    font=("Times", 10),
)

save_button.pack(side="left")




files_button = tk.Button(
    root,
    command=run_c,
    text="C >",
    width=1,
    bd=6,
    bg="#002200",
    fg="lightgrey",
    font=("Times", 10),
)

files_button.pack(side="left")





python_button = tk.Button(
    root,
    command=run_python,
    text="P >",
    width=1,
    bd=6,
    bg="grey",
    fg="cyan",
    font=("Times", 10),
)

python_button.pack(side="left")


files_button = tk.Button(
    root,
    command=clear_screen,
    text="Cls",
    width=1,
    bd=6,
    bg="darkred",
    fg="red",
    font=("Times", 10),
)

files_button.pack(side="left")







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
        item for item in all_words
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
            height=10,
            bg="#111122",
            fg="lightgrey",
            font=("Courier New", 10),
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


result_window.bind("<Return>", auto_indent)


result_window.bind("<Button-1>", goto_line_selected)

root.mainloop()
