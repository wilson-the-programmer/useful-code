import math
import random
import subprocess
import tempfile
import os
import io
import sys
import re
import threading
import keyword

import tkinter as tk
from tkinter import (
    filedialog,
    scrolledtext,
    colorchooser,
    simpledialog,
    messagebox
)

from tkinter.font import families

import webbrowser
import urllib.parse

import black




file_path = None


c_keywords = [
    "auto",
    "break",
    "case",
    "char",
    "const",
    "continue",
    "default",
    "do",
    "double",
    "else",
    "enum",
    "extern",
    "float",
    "for",
    "goto",
    "if",
    "inline",
    "int",
    "long",
    "register",
    "restrict",
    "return",
    "short",
    "signed",
    "sizeof",
    "static",
    "struct",
    "switch",
    "typedef",
    "union",
    "unsigned",
    "void",
    "volatile",
    "while",
]


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


def quick_hex(r, g, b):
	return f"#{r:02x}{g:02x}{b:02x}"
	


def dark_screen():
	global dark_screen
	current_widget = root.focus_get()
	bg_red = random.randint(0, 100)
	bg_green = random.randint(0, 100)
	bg_blue = random.randint(0, 100)
	fg_red = random.randint(170, 255)
	fg_green = random.randint(170, 255)
	fg_blue = random.randint(170, 255)
	back_c = quick_hex(bg_red, bg_green, bg_blue)
	fore_c = quick_hex(fg_red, fg_green, fg_blue)
	
	current_widget.config(
	    bg=back_c,
	    fg=fore_c
	)
	#dark_screen = True
	
	
def theme_forest():
	global dark_screen
	current_widget = root.focus_get()
	menu_bg = "#635951"
	menu_fg = "#e6ebf0"
	back_bg = "#353338"
	fore_fg = "#acb4bb"
	cursor_bg = "gold"
	menu.config(
	    bg=menu_bg,
	    fg=menu_fg
	)
	current_widget.config(
	    bg=back_bg,
	    fg=fore_fg,
	    insertbackground=cursor_bg
	
	)
	
	highlight_code_dark()
	dark_screen = True
	

def quick_hex(r, g, b):
	return f"#{r:02x}{g:02x}{b:02x}"
	


def random_back():
	current_window = root.focus_get()
	bg_red = random.randint(0, 255)
	bg_green = random.randint(0, 255)
	bg_blue = random.randint(0, 255)

	
	back_c = quick_hex(bg_red, bg_green, bg_blue)
	fore_c = current_window.cget("fg")
	
	
	current_window.config(
	    bg=back_c
	)
	
	current_window.delete(1.0, "2.end")
	current_window.insert(1.0, f"bg='{back_c}',\nfg='{fore_c}',")


def random_fore():
	current_window = root.focus_get()
	fg_red = random.randint(0, 255)
	fg_green = random.randint(0, 255)
	fg_blue = random.randint(0, 255)
	back_c = current_window.cget("bg")
	fore_c = quick_hex(fg_red, fg_green, fg_blue)
	
	current_window.config(
	    fg=fore_c
	)
	
	current_window.delete(1.0, "2.end")
	current_window.insert(1.0, f"bg='{back_c}',\nfg='{fore_c}',")
	

def random_expression():
	current_window = root.focus_get()
	func = random.choice(["×", "/", "+", "-"])
	num_1 = random.randint(1, 99)
	num_2 = random.randint(1, 99)
	express = f"{num_1} {func} {num_2} "
	current_window.insert("insert", f"{express}")



def format_python_code():
    current_widget = root.focus_get()
    def background_work():

        try:
            input_code = current_widget.get("1.0", "end-1c")
            reformatted_code = black.format_str(input_code, mode=black.FileMode())

            current_widget.delete("1.0", "end")
            current_widget.insert("1.0", reformatted_code)

        except:
            pass
    threading.Thread(target=background_work).start()


def indent_all():
    current_window = root.focus_get()
    content = current_window.get("1.0", "end-1c")
    lines = content.split("\n")
    indented = "\n".join(
        "    " + line if line.strip() != "" else line for line in lines
    )
    current_window.delete("1.0", "end")
    current_window.insert("1.0", indented)



def run_flake8():
    current_window = root.focus_get()

    def task():
        try:
            code = current_window.get("1.0", "end-1c")

            f = tempfile.NamedTemporaryFile(
                delete=False, suffix=".py", mode="w", encoding="utf-8"
            )
            f.write(code)
            f.close()

            result = subprocess.run(["flake8", f.name], capture_output=True, text=True)

            if result.stdout.strip():
                if current_window == editor:
                    result_window.insert(1.0, result.stdout)
                    result_window.focus_set()
                    root.after(100, format_flake8)
                    root.after(200, lambda: result_window.focus_set())

                    root.after(300, highlight_code_dark)

                else:
                    editor.insert(1.0, result.stdout)
                    editor.focus_set()
                    root.after(100, format_flake8)
                    root.after(200, lambda: editor.focus_set())
                    root.after(300, highlight_code)
            elif result.stderr.strip():
                if current_window == editor:
                    result_window.insert(1.0, result.stderr)
            else:
                if current_window == editor:
                    result_window.insert(1.0, "No issues found")

            os.unlink(f.name)

        except:
            pass

    threading.Thread(target=task, daemon=True).start()


def format_flake8():
    try:
        current_window = root.focus_get()

        text = current_window.get("1.0", "end")

        lines = text.splitlines()

        grouped = {}

        for line in lines:
            m = re.search(r"(.+?):(\d+):(\d+):\s+([A-Z]\d+)\s+(.*)", line)

            if not m:
                continue

            line_number = int(m.group(2))

            message = m.group(5).strip()

            if message:
                message = message[0].upper() + message[1:]

            if not message.endswith("."):
                message += "."

            grouped.setdefault(line_number, []).append(message)

        output = []

        output.append(f"Imperfections: {sum(len(v) for v in grouped.values())}")
        output.append("")

        for line_number in sorted(grouped):
            output.append(f"Line {line_number}:")
            output.append("")

            for msg in grouped[line_number]:
                output.append(f"• {msg}")

            output.append("")

        current_window.delete("1.0", "end")
        current_window.insert("1.0", "\n".join(output))

    except:
        pass


def highlight_line():
    w = root.focus_get()

    try:
        line_start = w.index("insert linestart")
        line_end = w.index("insert lineend")

        tag = "cursor_line"

        w.tag_add(tag, line_start, line_end)
        w.tag_config(tag, background="yellow", foreground="black")

    except:
        pass


def show_whitespaces(event=None):
    current_window = root.focus_get()
    current_window.tag_remove("trail_ws", "1.0", "end")

    text = current_window.get("1.0", "end-1c")
    lines = text.splitlines()

    for i, line in enumerate(lines, start=1):
        match = re.search(r"(?<=\S)[ \t]+$", line)
        if match:
            start = f"{i}.{match.start()}"
            end = f"{i}.{match.end()}"
            current_window.tag_add("trail_ws", start, end)

    current_window.tag_config("trail_ws", background="red")


def remove_whitespaces():
    current_window = root.focus_get()

    try:
        text = current_window.get("1.0", "end-1c")
        lines = text.splitlines()

        cleaned = [line.rstrip(" \t") for line in lines]

        current_window.delete("1.0", "end")
        current_window.insert("1.0", "\n".join(cleaned))

    except:
        pass


def goto_line_selected(event=None):
    highlight_code_dark()
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
        highlight_line()

    except:
        pass


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


def analyze():
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


# ---------------- Developer Tools ----------------


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
                        result_window.focus_set()
                        highlight_detect()
                        expand_window()
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
    if len(last_file_opened) > 0:
    	with open(last_file_opened, "w", encoding="utf-8") as file:
    		file.write(current_window.get("1.0", "end-1c"))
    else:
    	save_file()



def search_selected():
    try:
        widget = root.focus_get()
        text = widget.selection_get().strip()

        if not text:
            return

        if text.lower().endswith((".com", ".org", ".net", ".edu", ".gov", ".io")):
            webbrowser.open_new_tab("https://" + text)
        else:
            query = urllib.parse.quote_plus(text)
            webbrowser.open_new_tab(f"https://www.bing.com/search?q={query}")

    except:
        pass


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


def bg_color():
    current_window = root.focus_get()
    try:
        color = colorchooser.askcolor()[1]
        if not color:
            return
        current_window.config(bg=color)
    except:
        pass


def fg_color():
    current_window = root.focus_get()
    try:
        color = colorchooser.askcolor()[1]
        if not color:
            return
        current_window.config(fg=color)
    except:
        pass


def menu_bg():
    try:
        color = colorchooser.askcolor()[1]
        if not color:
            return
        menu.config(bg=color)
    except:
        pass


def menu_fg():
    try:
        color = colorchooser.askcolor()[1]
        if not color:
            return
        menu.config(fg=color)
    except:
        pass


def cursor_bg():
    current_window = root.focus_get()
    try:
        color = colorchooser.askcolor()[1]
        if not color:
            return
        current_window.config(insertbackground=color)
    except:
        pass


def get_colors(event=None):
    try:
        current_window = root.focus_get()

        menu_bg = menu.cget("bg")
        menu_fg = menu.cget("fg")

        bg = current_window.cget("bg")
        fg = current_window.cget("fg")

        try:
            cursor = current_window.cget("insertbackground")
        except:
            cursor = "default"

        output = (
            f'menu_bg = "{menu_bg}"\n'
            f'menu_fg = "{menu_fg}"\n'
            f'back_bg = "{bg}"\n'
            f'fore_fg = "{fg}"\n'
            f'cursor_bg = "{cursor}"\n'
        )

        editor.insert(1.0, f"{output}\n")

    except:
        pass


def color_line():
    current_window = root.focus_get()

    index = current_window.index("insert")
    line_start = index.split(".")[0] + ".0"

    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    color = f"#{r:02x}{g:02x}{b:02x}"

    tag_name = "rand_line"

    current_window.tag_remove(tag_name, "1.0", "end")
    current_window.tag_add(tag_name, line_start, index)
    current_window.tag_config(tag_name, foreground=color)

    current_window.insert("end", f"\ncolor : {color}")


def invert_colors():
    widget = root.focus_get()

    if not widget:
        return

    bg = widget.cget("bg")
    fg = widget.cget("fg")

    widget.config(bg=fg, fg=bg)



def set_font_size():
    global font_size
    widget = root.focus_get()

    if not widget:
        return

    size = simpledialog.askinteger(
        "Font Size", "Enter font size (6-15):", minvalue=6, maxvalue=15
    )

    if size is None:
        return

    widget.config(font=("Courier New", size))
    font_size = size



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
            root.geometry("460x480+0+0")

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



def reset_window():
	root.geometry("460x480+0+0")
	editor.config(height=8)
	result_window.config(height=6)

def highlight_code(event=None):
    current_window = root.focus_get()

    line = int(current_window.index("insert").split(".")[0])

    first = max(1, line - 28)
    last = line + 28

    region_start = f"{first}.0"
    region_end = f"{last}.end"

    for tag in ("kw", "var", "eq", "num", "str", "call"):
        current_window.tag_remove(tag, region_start, region_end)

    text = current_window.get(region_start, region_end)

    for k in keyword.kwlist + c_keywords:
        for m in re.finditer(rf"\b{re.escape(k)}\b", text):
            s = current_window.index(f"{region_start}+{m.start()}c")
            e = current_window.index(f"{region_start}+{m.end()}c")
            current_window.tag_add("kw", s, e)

    for m in re.finditer(r"\b([A-Za-z_]\w*)\s*=", text):
        s = current_window.index(f"{region_start}+{m.start(1)}c")
        e = current_window.index(f"{region_start}+{m.end(1)}c")
        current_window.tag_add("var", s, e)

    for m in re.finditer(r"=", text):
        s = current_window.index(f"{region_start}+{m.start()}c")
        current_window.tag_add("eq", s, f"{s}+1c")

    for m in re.finditer(r"\b\d+(\.\d+)?\b", text):
        s = current_window.index(f"{region_start}+{m.start()}c")
        e = current_window.index(f"{region_start}+{m.end()}c")
        current_window.tag_add("num", s, e)

    for m in re.finditer(r'"[^"\n]*"|\'[^\'\n]*\'', text):
        s = current_window.index(f"{region_start}+{m.start()}c")
        e = current_window.index(f"{region_start}+{m.end()}c")
        current_window.tag_add("str", s, e)

    for m in re.finditer(r"\b([A-Za-z_]\w*)\(", text):
        s = current_window.index(f"{region_start}+{m.start(1)}c")
        e = current_window.index(f"{region_start}+{m.end(1)}c")
        current_window.tag_add("call", s, e)

    current_window.tag_config("kw", foreground="red")
    current_window.tag_config("var", foreground="#5c4fad")
    current_window.tag_config("eq", foreground="darkred")
    current_window.tag_config("num", foreground="#018a5c")
    current_window.tag_config("str", foreground="#E67300")
    current_window.tag_config("call", foreground="blue")


# for dark background
def highlight_code_dark(event=None):
    current_window = root.focus_get()

    line = int(current_window.index("insert").split(".")[0])

    first = max(1, line - 28)
    last = line + 28

    region_start = f"{first}.0"
    region_end = f"{last}.end"

    for tag in ("kw", "var", "eq", "num", "str", "call"):
        current_window.tag_remove(tag, region_start, region_end)

    text = current_window.get(region_start, region_end)

    for k in keyword.kwlist + c_keywords:
        for m in re.finditer(rf"\b{re.escape(k)}\b", text):
            s = current_window.index(f"{region_start}+{m.start()}c")
            e = current_window.index(f"{region_start}+{m.end()}c")
            current_window.tag_add("kw", s, e)

    for m in re.finditer(r"\b([A-Za-z_]\w*)\s*=", text):
        s = current_window.index(f"{region_start}+{m.start(1)}c")
        e = current_window.index(f"{region_start}+{m.end(1)}c")
        current_window.tag_add("var", s, e)

    for m in re.finditer(r"=", text):
        s = current_window.index(f"{region_start}+{m.start()}c")
        current_window.tag_add("eq", s, f"{s}+1c")

    for m in re.finditer(r"\b\d+(\.\d+)?\b", text):
        s = current_window.index(f"{region_start}+{m.start()}c")
        e = current_window.index(f"{region_start}+{m.end()}c")
        current_window.tag_add("num", s, e)

    for m in re.finditer(r'"[^"\n]*"|\'[^\'\n]*\'', text):
        s = current_window.index(f"{region_start}+{m.start()}c")
        e = current_window.index(f"{region_start}+{m.end()}c")
        current_window.tag_add("str", s, e)

    for m in re.finditer(r"\b([A-Za-z_]\w*)\(", text):
        s = current_window.index(f"{region_start}+{m.start(1)}c")
        e = current_window.index(f"{region_start}+{m.end(1)}c")
        current_window.tag_add("call", s, e)

    current_window.tag_config("kw", foreground="#1fc7f5")
    current_window.tag_config("var", foreground="#ecb696")
    current_window.tag_config("eq", foreground="white")
    current_window.tag_config("num", foreground="#15d2bb")
    current_window.tag_config("str", foreground="#9ddba0")
    current_window.tag_config("call", foreground="gold")


def highlight_detect(event=None):
    if screen_dark:
        highlight_code_dark()
        editor.config(insertbackground="gold")
    else:
        highlight_code()
        editor.config(insertbackground="darkred")


def select_all_copy():
    widget = root.focus_get()

    if widget is None:
        return

    try:
        widget.tag_add("sel", "1.0", "end")
        widget.clipboard_clear()
        widget.clipboard_append(widget.get("1.0", "end-1c"))
        return
    except:
        pass

    try:
        widget.select_range(0, "end")
        widget.clipboard_clear()
        widget.clipboard_append(widget.get())
    except:
        pass


def edit_mode():
    try:
        editor.config(state=tk.NORMAL)
        result_window.config(state=tk.NORMAL)

    except:
        pass


def grey_theme():
    root.config(bg="#abe1da")
    menu.config(bg="#c7dddf", fg="#1f280a")
    editor.config(bg="#adb4c0", fg="#1a024b")

    editor.config(insertbackground="darkgrey")


def bash_theme():
    root.config(bg="#b1fbce")
    menu.config(bg="#b2cfcb", fg="#191218")
    editor.config(bg="black", fg="white")

    editor.config(insertbackground="orange")


def sky_theme():
    root.config(bg="#b8d7dd")
    menu.config(bg="#e3b09c", fg="#3c0b47")
    editor.config(bg="#a9fdf4", fg="#1c0e15")

    editor.config(insertbackground="darkred")


def read_only():
    current_window = root.focus_get()
    if current_window is None:
        return

    try:
        current_window.config(state=tk.DISABLED)
    except:
        pass


def prime_logarithms():
    current_window = root.focus_get()

    try:
        text = current_window.get("insert linestart", "insert lineend").strip()

        if "," in text:
            start, end = map(int, text.split(",", 1))
        else:
            start = 2
            end = int(text)

        if start > end:
            start, end = end, start

        def is_prime(n):
            if n < 2:
                return False
            if n == 2:
                return True
            if n % 2 == 0:
                return False
            i = 3
            while i * i <= n:
                if n % i == 0:
                    return False
                i += 2
            return True

        output = []
        output.append("=== Prime Logarithms ===")
        output.append("")
        output.append(f"Range: ({start}, {end})")
        output.append("")
        output.append(f"{'Prime':>8} {'ln(p)':>12}")

        theta = 0.0

        for p in range(start, end + 1):
            if is_prime(p):
                lp = math.log(p)
                theta += lp
                output.append(f"{p:>8} {lp:>12.6f}")

        output.append("")
        output.append("=== Chebyshev Theta ===")
        output.append(f"θ = {theta:.6f}")
        output.append(f"End - θ = {end - theta:.6f}")

        current_window.delete("insert linestart", "insert lineend")
        current_window.insert("insert linestart", "\n".join(output))

    except Exception as e:
        print(e)


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


def decrease_font():
    global font_size
    if font_size >= 7:
        font_size -= 1
    editor.config(font=("Courier New", font_size))


def increase_font():
    global font_size
    if font_size <= 7:
        font_size += 1
    editor.config(font=("Courier New", font_size))


font_styles = [
    "Times New Roman",
    "Ariel",
    "TkDefault",
    "Courier New",
    "AndroidClock",
    "Carrois Gothic SC",
    "Coming Soon",
    "Cutive Mono",
    "Dancing Script",
    "Droid Sans Mono",
    "Noto Sans Gothic",
    "Noto Sans Mono CJK JP",
    "Noto Sans Mono CJK HK",
    "Noto Serif CJK HK",
    "Roboto",
    "RobotoStatic",
    "Source Sans Pro",
    "Source Sans Pro SemiBold",
]





screen_dark = True

font_size = 8


# ---------------- UI ----------------

root = tk.Tk()

root.geometry("460x480+0+0")

editor = tk.Text(
    root,
    wrap=tk.WORD,
    padx=8,
    pady=8,
    bg = "#19002a",
    fg = "white",
    insertbackground="cyan",
    insertwidth=6,
    height=8,
    font=("Courier New", font_size),
    undo=True,
    bd=4,
)
editor.pack(
    side="bottom",
    expand=True,
    fill="both"
)





result_window = scrolledtext.ScrolledText(
    root,
    wrap="word",
    padx=8,
    pady=8,
    insertbackground="cyan",
    insertwidth=6,
    width=34,
    height=6,
    font=("Courier New", 7),
    bg = "#0c131c",
    fg = "#ffffd9"
)


result_window.pack(side="top", expand=True, fill="both")


menu = tk.Menu(
    root,
    bd=4,
    font=("Courier New", 11),
    bg="gold",
    fg="darkblue"
)



root.config(menu=menu)


file_menu = tk.Menu(menu, tearoff=0, font=("Courier New", 11))

menu.add_cascade(label="File", menu=file_menu)

file_menu.add_command(label="New", command=new_file)

file_menu.add_command(label="Open", command=open_file)


file_menu.add_command(label="Save", command=save_file)

file_menu.add_command(label="Save Last", command=save_last_opened)


file_menu.add_command(label="View File", command=open_file_from_cursor)

file_menu.add_command(label="Line Number", command=goto_line_num)

file_menu.add_command(label="Reset App Root", command=reset_window)

file_menu.add_command(label="Go to Top↑", command=go_to_top)

file_menu.add_command(label="Go to Bottom↓", command=go_to_bottom)

file_menu.add_command(label="Font Size", command=set_font_size)




edit_menu = tk.Menu(menu, tearoff=0, font=("Courier New", 11))

menu.add_cascade(label="Edit", menu=edit_menu)


edit_menu.add_command(label="Undo", command=undo_last)
edit_menu.add_command(label="Redo", command=redo_last)
edit_menu.add_command(label="Cut", command=cut_text)
edit_menu.add_command(label="Copy", command=copy_text)

edit_menu.add_command(label="Paste", command=paste_text)

edit_menu.add_command(label="Cut Above↑", command=cut_above)

edit_menu.add_command(label="Cut Below↓", command=cut_below)

edit_menu.add_command(label="Indent All →", command=indent_all)



edit_menu.add_command(label="SelectAll & Copy", command=select_all_copy)


edit_menu.add_command(label="Clear Output", command=clear_window)

math_menu = tk.Menu(menu, tearoff=0, font=("Courier New", 11))

menu.add_cascade(label="Math", menu=math_menu)


math_menu.add_command(label="List Primes", command=list_primes)

math_menu.add_command(label="Analyze Primes", command=analyze)

math_menu.add_command(label="Prime Logarithms", command=prime_logarithms)

math_menu.add_command(label="Check if Prime", command=check_if_prime)


color_menu = tk.Menu(menu, tearoff=0, font=("Courier New", 11))

menu.add_cascade(label="Col", menu=color_menu)

color_menu.add_command(label="Menu bg", command=menu_bg)

color_menu.add_command(label="Menu fg", command=menu_fg)

color_menu.add_command(label="Window bg", command=bg_color)

color_menu.add_command(label="Window fg", command=fg_color)

color_menu.add_command(label="Cursor Color", command=cursor_bg)

color_menu.add_command(label="Dark Screen", command=dark_screen)

color_menu.add_command(label="Invert bg/fg", command=invert_colors)

color_menu.add_command(label="Forest Theme", command=theme_forest)

color_menu.add_command(label="Color line", command=color_line)


color_menu.add_command(label="highlight_code_dark", command=highlight_code_dark)

color_menu.add_command(label="Get Colors", command=get_colors)


dev_menu = tk.Menu(menu, tearoff=0, font=("Courier New", 11))

menu.add_cascade(label="Dev", menu=dev_menu)

dev_menu.add_command(label="Run Python", command=run_python)

dev_menu.add_command(label="Flake8 Code", command=run_flake8)


dev_menu.add_command(label="Format Python", command=format_python_code)


dev_menu.add_command(label="Run C", command=run_c)

dev_menu.add_command(label="Edit Mode", command=edit_mode)

dev_menu.add_command(label="Read-Only", command=read_only)

dev_menu.add_command(label="Font[-1]", command=decrease_font)


dev_menu.add_command(label="Font[+1]", command=increase_font)


btn_frame = tk.Frame(root)
btn_frame.pack(side="left")

open_button = tk.Button(
    btn_frame,
    text="ls *",
    command=list_files,
    bd=4,
    bg="lightblue",
    width=1,
    font=("Courier New", 9),
)
open_button.pack(side="left")

view_button = tk.Button(
    btn_frame,
    text="View",
    command=open_file_from_cursor,
    bd=4,
    bg="black",
    fg="white",
    width=1,
    font=("Courier New", 9),
)
view_button.pack(side="left")

c_button = tk.Button(
    btn_frame,
    text="C>",
    command=run_c,
    bd=4,
    bg="gold",
    fg="#000044",
    width=1,
    font=("Courier New", 9),
)
c_button.pack(side="left")


python_button = tk.Button(
    btn_frame,
    text="P >",
    command=run_python,
    bd=4,
    bg="cyan",
    width=1,
    font=("Courier New", 9),
)

python_button.pack(side="left")

c_button = tk.Button(
    btn_frame,
    text="Save",
    command=save_last_opened,
    bd=4,
    bg="white",
    fg="darkgreen",
    width=1,
    font=("Courier New", 9),
)
c_button.pack(side="left")



expand_button = tk.Button(
    btn_frame,
    text="[]",
    command=expand_window,
    bd=4,
    bg="blue",
    fg="white",
    width=1,
    font=("Courier New", 9),
)
expand_button.pack(side="left")


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


editor.bind("<Return>", auto_indent)

editor.bind("<Button-1>", highlight_code_dark)


result_window.bind("<Return>", auto_indent)


result_window.bind("<Button-1>", goto_line_selected)

#theme_forest()

editor.focus_set()

root.mainloop()

