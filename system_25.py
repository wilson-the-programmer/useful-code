import io
import os
import sys
import subprocess
import threading
import tempfile
import math

import tkinter as tk
from tkinter import (
    filedialog,
    simpledialog,
    colorchooser
)

from pygments import lex

from pygments.lexers.python import PythonLexer

from pygments.styles import get_style_by_name



unix_words = [
    "cal",
    "cat",
    "cd",
    "chmod",
    "chown",
    "clear",
    "cmake",
    "cp",
    "cpplint",
    "date",
    "echo",
    "find",
    "flake8",
    "g++",
    "gcc",
    "git",
    "grep",
    "head",
    "kill",
    "less",
    "ls",
    "make",
    "mkdir",
    "more",
    "mv",
    "ps",
    "pwd",
    "python",
    "python3",
    "rm",
    "rmdir",
    "sort",
    "tail",
    "top",
    "touch",
    "wc",
    "whoami"
]


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


window_expanded = 0


def expand_window():
    global window_expanded

    current_window = root.focus_get()

    try:
        window_expanded += 1

        if window_expanded > 1:
            window_expanded = 0

        if window_expanded == 1:

            
            if current_window == editor:
                editor.config(height=12)
                result_window.config(height=1)
                #root.geometry("460x770+0+0")
                
            else:
                result_window.config(height=14)
                editor.config(heigh=1)
                #root.geometry("460x770+0+0")

        else:
            editor.config(heigh=8)
            result_window.config(heigh=6)
            root.geometry("690x720+0+0")

    except:
        pass


def expand_app_max():
    global window_expanded

    try:
        window_expanded += 1

        if window_expanded > 1:
            window_expanded = 0

        if window_expanded == 1:
        	root.geometry("460x790+0+0")
        else:
        	root.geometry("460x480+0+0")
    except:
    	pass




def quick_hex(r, g, b):
	return f"#{r:02x}{g:02x}{b:02x}"
	



def mandarin_translator():
    from pypinyin import pinyin, Style
    from deep_translator import GoogleTranslator

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


def cut_below(event=None):
    try:
        current_window = root.focus_get()

        current_window.delete("insert", "end")

    except:
        pass


def cut_above(event=None):
    try:
        current_window = root.focus_get()

        current_window.delete("1.0", "insert")

    except:
        pass


def goto_line_num(event=None):
    current_window = root.focus_get()
    try:
        line = simpledialog.askinteger("Go to line", "Enter line number:")

        if not line or line < 1:
            return

        current_window.mark_set("insert", f"{line}.0")
        current_window.see(f"{line}.0")

        current_window.tag_add("current_line", f"{line}.0", f"{line}.0 lineend")

        current_window.focus_set()

    except:
        pass


def go_to_top():
    current_window = root.focus_get()
    if current_window is None:
        return
    try:
        current_window.mark_set("insert", "1.0")
        current_window.see("1.0")
    except:
        pass


def go_to_bottom():
    current_window = root.focus_get()
    if current_window is None:
        return
    try:
        current_window.mark_set("insert", "end")
        current_window.see("end")
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


def list_primes():
    current_window = root.focus_get()

    try:
        text = current_window.get("insert linestart", "insert lineend").strip()

        if "," in text:
            start, end = map(int, text.split(",", 1))
        else:
            start = 0
            end = int(text)

        if start > end:
            start, end = end, start

        result = []

        for n in range(max(2, start), end + 1):
            prime = True
            for i in range(2, int(n**0.5) + 1):
                if n % i == 0:
                    prime = False
                    break
            if prime:
                result.append(str(n))

        current_window.insert("insert", f"\nPrimes = {result}\n")

    except Exception as e:
        print(e)


def check_if_prime():

    current_window = root.focus_get()

    try:
        line = current_window.get("insert linestart", "insert lineend").strip()
        if int(line) % 2 == 0:
            current_window.insert("insert", " : Dude this number is Even.\n")
        n = int(line)

        if n < 2:
            result = f"{n} = not prime"
        elif n == 2:
            result = "2 = prime"
        elif n % 2 == 0:
            result = f"{n} = not prime"
        else:
            i = 3
            is_prime = True

            while i * i <= n:
                if n % i == 0:
                    is_prime = False
                    break
                i += 2

            if is_prime:
                result = f"{n} = prime.\n"
            else:
                result = f"{n} = not prime.\n"

        current_window.delete("insert linestart", "insert lineend")
        current_window.insert("insert linestart", result)

    except:
        pass



def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def li_approx(x):
    steps = 1000
    total = 0.0
    dx = max(x - 2.0, 0.0) / steps

    for i in range(1, steps):
        t = 2.0 + i * dx
        if t > 1:
            total += dx / math.log(t)

    return total


def clear_window():
    current_window = root.focus_get()
    current_window.delete("1.0", tk.END)


def new_file():
    global file_path
    file_path = None
    editor.delete("1.0", tk.END)
    result_window.delete("1.0", tk.END)


def analyze_number():
    result_window.delete("1.0", tk.END)

    try:
        end = int(editor.get("insert linestart", "insert lineend").strip())
    except:
        end = 10000

    primes = 0
    last = 0

    gap_sum = 0.0
    gap_count = 0
    twin = 0
    max_gap = 0

    for n in range(1, end + 1):
        if is_prime(n):
            primes += 1

            if last:
                gap = n - last
                gap_sum += gap
                gap_count += 1
                if gap > max_gap:
                    max_gap = gap
                if gap == 2:
                    twin += 1

            last = n

    rng = end

    density = primes / rng
    expected = end / math.log(end)
    error = primes - expected
    rel = abs(error) / expected

    avg_gap = gap_sum / gap_count if gap_count else 0
    li = li_approx(end)
    li_error = primes - li

    norm_err = error / math.sqrt(end)

    result_window.insert(tk.END, "=== Prime Interval Summary ===\n\n")
    result_window.insert(tk.END, f"Range: (1, {end})\n")
    result_window.insert(tk.END, f"Primes: {primes}\n")
    result_window.insert(tk.END, f"Expected π(x): {expected:.2f}\n")
    result_window.insert(tk.END, f"Error: {error:.2f}\n")
    result_window.insert(tk.END, f"Relative Error: {rel:.6f}\n")
    result_window.insert(tk.END, f"Density: {density:.6f}\n")
    result_window.insert(tk.END, f"Average Gap: {avg_gap:.3f}\n")
    result_window.insert(tk.END, f"Max Gap: {max_gap}\n")
    result_window.insert(tk.END, f"Twin Primes: {twin}\n\n")

    result_window.insert(tk.END, "=== Analytic Layer ===\n\n")
    result_window.insert(tk.END, f"Li(x): {li:.2f}\n")
    result_window.insert(tk.END, f"Li Error: {li_error:.2f}\n")
    result_window.insert(tk.END, f"Normalized Error: {norm_err:.6f}\n")


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
    if len(last_file_opened) > 0:
    	with open(last_file_opened, "w", encoding="utf-8") as file:
    		file.write(current_window.get("1.0", "end-1c"))
    else:
    	save_file()




def apply_syntax_single(event=None):

    style = get_style_by_name(pygment_theme)

    line = editor.index(tk.INSERT).split(".")[0]

    start = f"{line}.0"
    end = f"{line}.end"

    editor.tag_remove("syntax", start, end)

    text = editor.get(start, end)

    position = start

    for token, value in lex(text, PythonLexer()):
        next_position = f"{position}+{len(value)}c"

        color = None

        token_name = str(token)

        for key, style_value in style.styles.items():
            if str(key) == token_name:
                if style_value:
                    for item in style_value.split():
                        if item.startswith("#"):
                            color = item
                            break

        if color:
            editor.tag_configure(token_name, foreground=color)
            editor.tag_add(token_name, position, next_position)

        position = next_position



def apply_syntax_all(event=None):

    code = editor.get("1.0", tk.END)

    editor.tag_remove("all", "1.0", tk.END)

    style = get_style_by_name(pygment_theme)

    for token, value in lex(code, PythonLexer()):
        tag = str(token)

        color = None

        for key, style_value in style.styles.items():
            if str(key) == tag:
                if style_value:
                    parts = style_value.split()
                    for part in parts:
                        if part.startswith("#"):
                            color = part
                            break

        if color:
            start = editor.index(tk.INSERT)
            editor.tag_configure(tag, foreground=color)

    position = "1.0"

    for token, value in lex(code, PythonLexer()):
        end = f"{position}+{len(value)}c"

        tag = str(token)

        color = None

        for key, style_value in style.styles.items():
            if str(key) == tag:
                if style_value:
                    parts = style_value.split()
                    for part in parts:
                        if part.startswith("#"):
                            color = part
                            break

        if color:
            editor.tag_configure(tag, foreground=color)
            editor.tag_add(tag, position, end)

        position = end





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


def run_python():
    current_window = root.focus_get()
    code = current_window.get("1.0", tk.END)

    output = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = output

    try:
        exec(code)

    except Exception as e:
        output.write(f"{type(e).__name__}: {e}")

    finally:
        sys.stdout = old_stdout

        if current_window == editor:
            result_window.delete(1.0, "end")
            result_window.insert(1.0, output.getvalue())
        else:
            editor.delete(1.0, "end")
            editor.insert(1.0, output.getvalue())

pygment_theme = "one-dark"

root = tk.Tk()

root.geometry("690x720")

editor = tk.Text(
    root,
    wrap="word",
    undo=True,
    padx=10,
    pady=10,
    height=7,
    insertwidth=5,
    insertbackground="cyan",
    bd=4,
    font=("Courier New", 9),
    bg="black",
    fg="white",
)

editor.pack(expand=True, fill="both", side="top")

result_window = tk.Text(
    root,
    wrap="word",
    padx=10,
    pady=10,
    height=5,
    insertwidth=5,
    bd=4,
    font=("Courier New", 9),
)

result_window.pack(expand=True, fill="both", side="top")



menu = tk.Menu(
    root,
    bd=4,
    font=("Courier New", 11),
    bg="black",
    fg="grey"
)



root.config(menu=menu)


file_menu = tk.Menu(
    menu,
    tearoff=0,
    font=("Courier New", 12)
)

menu.add_cascade(
    label="File",
    menu=file_menu,
    font=("Courier New", 12)
)

file_menu.add_command(label="New File", command=new_file)

file_menu.add_command(label="Open", command=open_file)


file_menu.add_command(label="Save", command=save_file)

file_menu.add_command(label="Save Last", command=save_last_opened)

file_menu.add_command(label="Line #", command=goto_line_num)

file_menu.add_command(label="Go To Top", command=go_to_top)

file_menu.add_command(label="Go To Bottom", command=go_to_bottom)




file_menu.add_command(label="List Files", command=list_files)

file_menu.add_command(label="View File", command=open_file_from_cursor)

file_menu.add_command(label="Highlight Python Code", command=apply_syntax_all)

edit_menu = tk.Menu(
    menu,
    tearoff=0,
    font=("Courier New", 12)
)

menu.add_cascade(label="Edit", menu=edit_menu)


edit_menu.add_command(label="Undo", command=undo_last)
edit_menu.add_command(label="Redo", command=redo_last)
edit_menu.add_command(label="Cut", command=cut_text)
edit_menu.add_command(label="Copy", command=copy_text)

edit_menu.add_command(label="Paste", command=paste_text)

edit_menu.add_command(label="Cut↑", command=cut_above)

edit_menu.add_command(label="Cut↓", command=cut_below)

extra_menu = tk.Menu(
    menu,
    tearoff=0,
    font=("Courier New", 12)
)

menu.add_cascade(label="Extra", menu=extra_menu)


extra_menu.add_command(label="Analize Number", command=analyze_number)

extra_menu.add_command(label="List Primes a, b", command=list_primes)


extra_menu.add_command(label="Check if Prime", command=check_if_prime)

extra_menu.add_command(label="Chinese", command=mandarin_translator)


files_button = tk.Button(
    root,
    command=list_files,
    text="ls *",
    bd=8,
    width=1,
    bg="#000078",
    fg="lightgrey",
    font=("Times", 10),
)

files_button.pack(side="left")

view_button = tk.Button(
    root,
    command=open_file_from_cursor,
    text="View",
    bd=8,
    width=1,
    bg="black",
    fg="lightgrey",
    font=("Times", 10),
)

view_button.pack(side="left")


c_button = tk.Button(
    root,
    command=run_c,
    text="C >",
    bd=8,
    width=2,
    bg="#002200",
    fg="lightgreen",
    font=("Times", 10),
)

c_button.pack(side="left")

python_button = tk.Button(
    root,
    command=run_python,
    text="P >",
    bd=8,
    width=2,
    bg="lightblue",
    fg="darkblue",
    font=("Times", 10),
)

python_button.pack(side="left")


copy_button = tk.Button(
    root,
    command=clear_window,
    text="Clr",
    bd=8,
    width=1,
    bg=quick_hex(100,0,0),
    fg="red",
    font=("Times", 10),
)

copy_button.pack(side="left")

paste_button = tk.Button(
    root,
    command=expand_window,
    text="[]",
    bd=8,
    width=1,
    bg="lightgreen",
    fg="#004200",
    font=("Times", 10),
)

paste_button.pack(side="left")


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


editor.bind("<KeyRelease>", apply_syntax_single)

editor.bind("<Button-1>", apply_syntax_single)

editor.bind("<Return>", auto_indent)


editor.focus_set()

root.mainloop()
