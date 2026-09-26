

import tempfile
import sys
import io
import os
import subprocess
import traceback
import threading
import random

import tkinter as tk

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
    "bash",
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


pygments_styles = [
    "abap",
    "algol",
    "algol_nu",
    "arduino",
    "autumn",
    "bw",
    "borland",
    "coffee",
    "colorful",
    "default",
    "dracula",
    "emacs",
    "friendly_grayscale",
    "friendly",
    "fruity",
    "github-dark",
    "gruvbox-dark",
    "gruvbox-light",
    "igor",
    "inkpot",
    "lightbulb",
    "lilypond",
    "lovelace",
    "manni",
    "material",
    "monokai",
    "murphy",
    "native",
    "nord-darker",
    "nord",
    "one-dark",
    "paraiso-dark",
    "paraiso-light",
    "pastie",
    "perldoc",
    "rainbow_dash",
    "rrt",
    "sas",
    "solarized-dark",
    "solarized-light",
    "staroffice",
    "stata-dark",
    "stata-light",
    "tango",
    "trac",
    "vim",
    "vs",
    "xcode",
    "zenburn",
]


my_style = "material"





def generate_words(event=None):
    current_widget = root.focus_get()
    prefix = current_widget.get("insert linestart", "insert lineend").strip()
    file_path = "wordnet_word_list.txt"
    with open(file_path, "r") as file:
        content = file.read()
        word_list = content.split()
        matching_words = [w for w in word_list if w.startswith(prefix)]
        if matching_words:
            current_widget.delete("insert linestart", tk.END)
            current_widget.insert("insert lineend", "\n".join(matching_words))
            print_total_lines()

        else:
            pass





def highlight_line(event=None):
    current_widget = text_entry
    current_bg = current_widget.cget("background")
    current_fg = current_widget.cget("foreground")
        
    current_widget.tag_remove("highlight", 1.0, "end")
    current_widget.tag_add("highlight", "insert linestart", "insert lineend+1c")
    current_widget.tag_remove("highlight", 1.0, "end")
    current_widget.tag_configure(
        "highlight", background=current_fg, foreground=current_bg
    )




def choose_font_size():
    try:
        current_widget = root.focus_get()
        font_size = simpledialog.askinteger("Font Size Integer", "Font Size:")
        current_widget.config(font=("Hack", font_size))
    except:
        pass

def select_all_copy():
    select_all()
    copy()

def select_all():
    current_widget = root.focus_get()
    current_widget.tag_add("sel", "1.0", "end+1c")




def get_colors():
    current_widget = root.focus_get()

    root_color = root.cget("bg")
    back = current_widget.cget("background")
    fore = current_widget.cget("foreground")

    current_widget.insert("insert", f"\nRoot = {root_color}\nbg = {back}\nfg = {fore}")


def random_light_screen():
    current_widget = root.focus_get()
    bg_color = "#{:02x}{:02x}{:02x}".format(
        random.randint(140, 255), random.randint(140, 255), random.randint(140, 255)
    )
    fg_color = "#{:02x}{:02x}{:02x}".format(
        random.randint(0, 140), random.randint(0, 140), random.randint(0, 140)
    )
    current_widget.config(bg=bg_color, fg=fg_color)
    output_window.delete(1.0, "2.end")
    output_window.insert(1.0, f"bg='{bg_color},\nfg={fg_color}")



def random_theme():
    global my_style
    random_style = random.choice(pygments_styles)
    theme = random_style
    my_style = theme
    style_label = tk.Label(
        root,
        bg="white",
        fg="darkgreen",
        text=f"Style: {theme}      "
    )
    style_label.place(x=960, y=5)
    highlight_code()


def check_python(event=None):
    current_window = root.focus_get()
    code = current_window.get(1.0, "end")
    try:
        exec(code, globals(), locals())
        output_window.delete(1.0, "end")
        
    except Exception as e:
        traceback_info = traceback.format_exc()
        lines = traceback_info.strip().split("\n")
        filtered = []
        skipping = True
        for line in lines:
            if "<string>" in line or "SyntaxError" in line or "NameError" in line:
                skipping = False
            if not skipping:
                filtered.append(line)
                final_output = "\n".join(filtered)

        output_window.delete(1.0, "end")
        output_window.insert(1.0, final_output)



last_file_opened = ""

def open_file(event=None):
    global last_file_opened
    global highlight_mode
    global command_mode
    
    current_window = root.focus_get()

    file_path = filedialog.askopenfilename(
        filetypes=[
            ("Python", "*.py*"),
            ("Rust", "*.rs*"),
            ("C++", "*.cpp*"),
            ("Text", "*.txt"),
            ("All", "*")
        ]
    )

    if file_path:
        last_file_opened = file_path.split("/")[-1]
        with open(file_path, "r") as file:
            content = file.read()
            current_window.delete("1.0", tk.END)
            current_window.insert(tk.INSERT, f"\n{content}")
            output_window.delete(1.0, "1.end")
            output_window.insert(1.0, last_file_opened)

        highlight_mode = False
        command_mode = False

        highlight_toggle_button.config(
            text="Pygment:Off",
            bg="lightgrey"
        )
        unix_toggle_button.config(
            text="Unix:Off",
            bg="lightgrey"
        )
        
    show_last_file()


def show_last_file():
    file_label = tk.Label(
        root,
        bg="white",
        fg="blue",
        text=f"File: '{last_file_opened}'"
    )
    file_label.place(x=300, y=5)
    
    root.after(1200, clear_file_lable)



def open_file_from_cursor(event=None):
    global last_file_opened
    global highlight_mode
    global command_mode
    
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
        
        highlight_mode = False
        command_mode = False

        highlight_toggle_button.config(
            text="Pygment:Off",
            bg="lightgrey"
        )
        unix_toggle_button.config(
            text="Unix:Off",
            bg="lightgrey"
        )
        show_last_file()


    except:
        pass
        

def save_file(event=None):
    current_window = root.focus_get()
    filename = filedialog.asksaveasfilename(defaultextension=".txt")

    if filename:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(current_window.get("1.0", "end-1c"))

    file_label = tk.Label(
        root,
        bg="white",
        fg="blue",
        text=f"File: '{last_file_opened}' Saved."
    )
    file_label.place(x=300, y=5)
    
    root.after(1200, clear_file_lable)




def clear_file_lable():
    file_label = tk.Label(
        root,
        bg="white",
        fg="darkblue",
        text=f"                                              "
    )
    file_label.place(x=300, y=5)


def save_last_opened(event=None):
    current_window = root.focus_get()
    
    page = current_window.get("1.0", "end-1c")
    
    with open(last_file_opened, "w", encoding="utf-8") as file:
        file.write(page)
            
    file_label = tk.Label(
        root,
        bg="white",
        fg="blue",
        text=f"File: '{last_file_opened}' Saved."
    )
    file_label.place(x=300, y=5)
    
    root.after(1200, clear_file_lable)
    

    try:
        if last_file_opened.endswith(".cpp"):
            with open("qt6_temp.cpp", "w", encoding="utf-8") as tFile:
                tFile.write(page)
                tFile.close()
    except:
        pass




def update_data(event=None):
    get_position()
    check_highlight_mode()
    

def choose_font_size():
    global font_size
    current_widget = root.focus_get()
    font_size = simpledialog.askinteger("Font Size Integer", "Font Size:")
    current_widget.config(font=("Hack", font_size))
 

current_language = "Text"

def detect_language(event=None):
    global current_language

    if "stdio.h" in editor.get(1.0, "end"):
        current_language = "C"
    elif "<iostream>" in editor.get(1.0, "end"):
        current_language = "C++"
    elif "#!/bin/bash" in editor.get(1.0, "end"):
        current_language = "Bash"
    elif "fn main" in editor.get(1.0, "end"):
        current_language = "Rust"
    elif "def" in editor.get(1.0, "end"):
        current_language = "Python3"
    elif "func main" in editor.get(1.0, "end"):
        current_language = "GoLang"
    elif "function" in editor.get(1.0, "end"):
        current_language = "JavaScript"
    elif "<QApplication>" in editor.get(1.0, "end"):
        current_language = "C++ Qt6"
    else:
        current_language = "text    "
    language_label = tk.Label(
        root,
        bg="white",
        fg="blue",
        text=f"Languade: {current_language}      "
    )
    language_label.place(x=600, y=5)




def get_line_amount(event=None):
    current_widget = root.focus_get()
    
    lines = len(current_widget.get(1.0, "end").splitlines())
    language_label = tk.Label(
        root,
        bg="lightgrey",
        text=f"Line Amount: {lines}   "
    )
    language_label.place(x=800, y=5)
    


window_expanded = 0

def expand_window():
    global window_expanded

    try:
        window_expanded += 1

        if window_expanded > 1:
            window_expanded = 0

        if window_expanded == 1:
            editor.config(height=28)
                

        else:
            editor.config(heigh=14)

    except:
        pass



def get_position(event=None):
    current_widget = root.focus_get()
	
    line = current_widget.index("insert").split(".")[0]
    line_position = current_widget.index("insert").split(".")[1]
    line_amount = len(current_widget.get(1.0, "end").splitlines())

    
    cursor_label = tk.Label(
        root,
        bg="yellow",
        text=f"Line/Total: {line}/{line_amount}, Col: {line_position}      "
    )
    cursor_label.place(x=100, y=5)





def detect_command(event=None):
    current_window = root.focus_get()
    cmd = current_window.get("insert linestart", "insert lineend").strip()
    for c in unix_words:
        if c in cmd:
            unix_command()



def numToHex():
    current_window = root.focus_get()
    try:
        num = int(current_window.get("insert linestart", "insert lineend").strip())
        current_window.insert("insert", f" = {hex(num)[2:]}")
    except Exception as e:
        output_window.insert(1.0, e)


def hexToNum():
    current_window = root.focus_get()
    try:
        hexValue = current_window.get("insert linestart", "insert lineend").strip()
        current_window.insert("insert", f" = {int(hexValue, 16)}")
    except Exception as e:
        output_window.insert(1.0, e)


def rgbToHex(r, g, b):
    try:
        rgb = editor.get("insert linestart", "insert lineend").strip()
        hex_code = f"#{r:02x}{g:02x}{b:02x}"
        
        editor.insert(1.0, f" = {hex_code}")
    except:
        pass
    


cIndex = 0

def last_command(event=None):
    global cIndex
    
    if len(recent_commands) > 0:
        cIndex -= 1
    if cIndex == -(len(recent_commands)):
        cIndex = 0
    if len(recent_commands) > 0:
        editor.delete("insert linestart", "insert lineend")
        editor.insert("insert", recent_commands[cIndex])
        

recent_commands = []

def unix_command():
    current_window = root.focus_get()
    
    command = current_window.get("insert linestart", "insert lineend").strip()
    
    recent_commands.append(command)
    if len(recent_commands) > 5:
        recent_commands.pop(0)

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
    



def smart_tab(event=None):
    current_widget = root.focus_get()
    char_left = current_widget.get("insert-1c", "insert")
    text = current_widget.get("insert linestart", "insert lineend").strip()
    try:
        if text:
            last_word = text.split()[-1]
            last_char = text.split()[-1][-1]
        for i in [":", "(", "["]:
            if i == char_left:
                root.after(60, lambda: current_widget.insert(tk.INSERT, "    "))
    except:
        pass



def auto_indent(event=None):
    check_command_mode()
    check_python_mode()
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


def random_root():
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)
    color = f"#{red:02x}{green:02x}{blue:02x}"
    root.config(bg=color)
    output_window.delete(1.0, "1.end")
    output_window.insert(1.0, f"root_bg = {color}\n")
    

def random_screen():
    current_window = root.focus_get()
    bg_red = random.randint(0, 55)
    bg_green = random.randint(0, 55)
    bg_blue = random.randint(0, 55)
    bg_color = f"#{bg_red:02x}{bg_green:02x}{bg_blue:02x}"
    
    fg_red = random.randint(200, 255)
    fg_green = random.randint(200, 255)
    fg_blue = random.randint(200, 255)
    fg_color = f"#{fg_red:02x}{fg_green:02x}{fg_blue:02x}"
    
    cursor_bg = random.choice([
        "orange",
        "lightyellow",
        "gold",
        "lightgrey",
        "white",
        "cyan"
    ])
    
    current_window.config(
        bg=bg_color,
        fg=fg_color,
        insertbackground=cursor_bg
    )
    output_window.delete(1.0, "3.end")
    output_window.insert(1.0, f"bg = {bg_color}\nfg = {fg_color}\nCursor = {cursor_bg}")




def run_bash():
	script = editor.get(1.0, "end")
	try:
		result = subprocess.run(
		    ["bash"],
		    input=script,
		    text=True,
		    #shell=True,
		    capture_output=True,
		    timeout=30
		)
		
		output = result.stdout
		error = result.stderr
	except subprocess.TimeoutExpired:
		output = "Error: Script Execution timed out."
	except Exception as e:
		output = f"Error: {e}"
		
	output_window.delete(1.0, "end")
	output_window.insert(1.0, output + error)


def run_c(event=None):
    current_window = root.focus_get()

    def task():
        try:
            code = current_window.get(1.0, "end")
            
            f = tempfile.NamedTemporaryFile(
                suffix=".c",
                mode="w",
                encoding="utf-8",
                delete=False
            )

            f.write(code)
            f.close()

            exe = f.name + ".out"

            try:
                comp = subprocess.run(
                    ["gcc", f.name, "-o", exe],
                    capture_output=True,
                    text=True
                )
                
                if comp.returncode != 0:
                    output_window.delete(1.0, "end")
                    output_window.insert(1.0, comp.stderr)
                    return 
                
                run = subprocess.run(
                    [exe],
                    capture_output=True,
                    text=True
                )

                output_window.delete(1.0, "end")
                output_window.insert(1.0, run.stdout)

            finally:
                if os.path.exists(f.name):
                    os.unlink(f.name)

                if os.path.exists(exe):
                    os.unlink(exe)

        except Exception as e:
            output_window.delete(1.0, "end")
            output_window.insert(1.0, e)

    threading.Thread(
        target=task,
        daemon=True
    ).start()



def run_cpp(event=None):
    current_window = root.focus_get()

    def task():
        try:
            code = current_window.get(1.0, "end")
            
            f = tempfile.NamedTemporaryFile(
                suffix=".cpp",
                mode="w",
                encoding="utf-8",
                delete=False
            )

            f.write(code)
            f.close()

            exe = f.name + ".out"

            try:
                cpp = subprocess.run(
                    ["g++", f.name, "-o", exe],
                    capture_output=True,
                    text=True
                )

                if cpp.returncode != 0:
                    output_window.delete(1.0, "end")
                    output_window.insert(1.0, cpp.stderr)
                    return

                r = subprocess.run(
                    [exe],
                    capture_output=True,
                    text=True
                )

                output_window.delete(1.0, "end")
                output_window.insert(1.0, r.stdout + r.stderr)

            finally:
                if os.path.exists(f.name):
                    os.unlink(f.name)

                if os.path.exists(exe):
                    os.unlink(exe)

        except Exception as e:
            output_window.delete(1.0, "end")
            output_window.insert(1.0, e)

    threading.Thread(
        target=task,
        daemon=True
    ).start()

"""

def run_cpp_app(event=None):
    current_window = root.focus_get()    

    try:
        
        file = current_window.get("insert linestart", "insert lineend").strip()

        eFile = file + ".out"
        
        extra_window.insert(1.0, f"g++ {file} -o {eFile} $(pkg-config --cflags --libs Qt6Widgets) -lqtermwidget6 && ./{eFile}")
        extra_window.focus_set()
        extra_window.see("insert")
        unix_command()
        #editor.focus_set()
        

    except Exception as e:
        output_window.insert(1.0, e)
        


  Reminder:

    this version below is pretty good

"""

def run_cpp_app(event=None):
    current_window = root.focus_get()    
    
    try:
        code = editor.get(1.0, "end")
        tFile = "qt6_temp.cpp"
        
        with open(tFile, "w") as f:
            f.write(code)
            f.close()
            
        eFile = tFile.replace(".cpp", "")
        
        extra_window.delete(1.0, "end")
        extra_window.insert(1.0, f"g++ {tFile} -o {eFile} $(pkg-config --cflags --libs Qt6Widgets) -lqtermwidget6 && ./{eFile}")
        extra_window.focus_set()
        extra_window.see("insert")
        unix_command()
        
        
        
        
        #root.after(300, lambda : editor.focus_set())
        
        

    except Exception as e:
        output_window.insert(1.0, e)
        





def run_rust(event=None):
    current_window = root.focus_get()

    def task():
        try:
            code = current_window.get(1.0, "end")
            
            f = tempfile.NamedTemporaryFile(
                suffix=".rs",
                mode="w",
                encoding="utf-8",
                delete=False
            )

            f.write(code)
            f.close()

            exe = f.name + ".out"

            try:
                c = subprocess.run(
                    ["rustc", f.name, "-o", exe],
                    capture_output=True,
                    text=True
                )

                if c.returncode != 0:
                    output_window.delete(1.0, "end")
                    output_window.insert(1.0, c.stderr)
                    return


                r = subprocess.run(
                    [exe],
                    capture_output=True,
                    text=True
                )

                output_window.delete(1.0, "end")
                output_window.insert(1.0, r.stdout)

            finally:
                if os.path.exists(f.name):
                    os.unlink(f.name)

                if os.path.exists(exe):
                    os.unlink(exe)

        except Exception as e:
            output_window.delete(1.0, "end")
            output_window.insert(1.0, e)

    threading.Thread(
        target=task,
        daemon=True
    ).start()


def run_golang(event=None):
    current_window = root.focus_get()

    def task():
        try:
            code = current_window.get(1.0, "end")
            
            f = tempfile.NamedTemporaryFile(
                suffix=".go",
                mode="w",
                encoding="utf-8",
                delete=False
                
            )

            f.write(code)
            f.close()

            try:
                c = subprocess.run(
                    ["go", "run", f.name],
                    capture_output=True,
                    text=True
                )
                
                output = c.stdout
                error = c.stderr

                if c.returncode != 0:
                    output_window.delete(1.0, "end")
                    output_window.insert(1.0, error)
                    return

                output_window.delete(1.0, "end")
                output_window.insert(1.0, output + error)

            finally:
                if os.path.exists(f.name):
                    os.unlink(f.name)


        except Exception as e:
            output_window.delete(1.0, "end")
            output_window.insert(1.0, e)


    threading.Thread(target=task, daemon=True).start()


def run_javascript(event=None):
    current_window = root.focus_get()

    def task():
        try:
            code = current_window.get(1.0, "end")
            f = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".js",
                mode="w",
                encoding="utf-8"
            )

            f.write(code)
            f.close()

            try:
                c = subprocess.run(
                    ["node", f.name],
                    capture_output=True,
                    text=True
                )

                if c.returncode != 0:
                    output_window.delete(1.0, "end")
                    output_window.insert(1.0, c.stderr)
                    return

                output_window.delete(1.0, "end")
                output_window.insert(1.0, c.stdout)

            finally:
                if os.path.exists(f.name):
                    os.unlink(f.name)


        except Exception as e:
            output_window.delete(1.0, "end")
            output_window.insert(1.0, e)


    threading.Thread(
        target=task,
        daemon=True
    ).start()



def run_python_partial(event=None):
    current_window = root.focus_get()
    code = current_window.get("1.0", "insert")

    output = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = output

    try:
        exec(code)

    except Exception as e:
        output.write(f"{type(e).__name__}: {e}")

    finally:
        sys.stdout = old_stdout
        
        current_window.delete("insert", "end")

        current_window.insert("insert", f"\n\n========================================\nPython3 Output:\n========================================\n\n{output.getvalue()}\n\n.........................................")


def run_python(event=None):
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

        output_window.delete(1.0, "end")
        output_window.insert(1.0, output.getvalue())
    
    

def highlight_code_single(event=None):
    current_window = root.focus_get()
    style = get_style_by_name(my_style)

    line = current_window.index("insert").split(".")[0]

    start = f"{line}.0"
    end = f"{line}.end"

    current_window.tag_remove("syntax", start, end)

    text = current_window.get(start, end)

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
            current_window.tag_configure(token_name, foreground=color)
            current_window.tag_add(token_name, position, next_position)

        position = next_position


def highlight_code(event=None):
	
    current_window = root.focus_get()

    code = current_window.get("1.0", tk.END)

    current_window.tag_remove("all", "1.0", tk.END)

    style = get_style_by_name(my_style)

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
            start = current_window.index(tk.INSERT)
            current_window.tag_configure(tag, foreground=color)

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
            current_window.tag_configure(tag, foreground=color)
            current_window.tag_add(tag, position, end)

        position = end



def undo_last(event=None):
    current_window = root.focus_get()
    try:
        current_window.edit_undo()
    except:
        pass


def redo_last():
    current_window = root.focus_get()
    try:
        current_window.edit_redo()
    except:
        pass



def go_to_line(event=None):
    current_widget = root.focus_get()
    line_number = simpledialog.askinteger("Go To Line", "Enter line number:")
    if line_number is not None:
        line = float(line_number)
        current_widget.mark_set("insert", line)
        current_widget.see(line)


def list_files(event=None):
    current_window = root.focus_get()
    last_location = current_window.index("insert")
    line_content = current_window.get("insert linestart", "insert lineend")
    letter = line_content.strip().lower()
    process = subprocess.Popen(
        ["ls"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True
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

def clear_window(event=None):
    current_window = root.focus_get()
    current_window.delete(1.0, "end")


def invert_screen():
    global my_style
    current_window = root.focus_get()
    
    current_window.config(
        bg=current_window.cget("fg"),
        fg=current_window.cget("bg"),
        insertbackground="grey",
    )
    if current_window == editor:
        if my_style != "lightbulb":
            my_style = "lightbulb"
        else:
            if my_style != "tango":
                my_style = "tango"







highlight_mode = True

def toggle_highlight_mode():
    global highlight_mode
    highlight_mode = not highlight_mode

    if highlight_mode:
        highlight_toggle_button.config(
            text="Pygment:On",
            bg="lightgreen"
        )
    else:
        highlight_toggle_button.config(
            text="Pygment:Off",
            bg="lightgrey"
        )


def check_highlight_mode(event=None):
    if highlight_mode:
        highlight_code_single()




command_mode = True

def toggle_command_mode():
    global command_mode
    command_mode = not command_mode

    if command_mode:
        unix_toggle_button.config(
            text="Unix:On",
            bg="lightgreen"
        )
    else:
        unix_toggle_button.config(
            text="Unix:Off",
            bg="lightgrey"
        )


def check_command_mode(event=None):
    if command_mode:
        detect_command()



python_mode = False

def toggle_pymode():
    global python_mode
    python_mode = not python_mode
    
    if python_mode:
        python_button.config(
            bg="lightgreen"
        )
        pymode_button.config(
            text="PMode: On",
            bg="lightgreen"
        )
    else:
        python_button.config(
            bg="lightgrey"
        )
        pymode_button.config(
            text="PMode: Off",
            bg="lightgrey"
        )


def check_python_mode(event=None):
    if python_mode:
        check_python()

def tuple_to_hex():
    current_widget = root.focus_get()
    rgb_str = current_widget.get("insert linestart", "insert lineend").strip()
    rgb_values = tuple(map(int, rgb_str.split(",")))
    hex_color = "#{:02x}{:02x}{:02x}".format(*rgb_values)
    current_widget.insert(tk.INSERT, f" = '{hex_color}'\n")



def eval_exp():
    current_window = root.focus_get()
    try:
        exp = current_window.get("insert linestart", "insert").strip().replace("x", "*").replace("t", "*").replace("d", "/").replace("p", "+").replace("m", "-").replace("e", "**")
        ans = eval(exp)
        current_window.delete("insert", "insert lineend")
        current_window.insert("insert", f" = {ans}")
        
    except:
        pass
        

def quick_hex(r,g,b):
    return f"#{r:02x}{g:02x}{b:02x}"

def show_color():    
    try:
        current_window = root.focus_get()
        color = current_window.get("insert linestart", "insert lineend").strip()
        if "#" not in color:
            color = "#" + current_window.get("insert linestart", "insert lineend").strip()
        output_window.config(bg=color)
        
    except Exception as e:
        output_window.insert(1.0, f"error:\n{e}\n")
    
       
def reset_editor():
    editor.config(
        bg="black",
        fg="white",
        insertbackgroun="cyan"
    )
    

def cut_above():
    current_window = root.focus_get()
    current_window.delete(1.0, "insert")

def cut_below():
    current_window = root.focus_get()
    current_window.delete("insert", "end")

def random_tuple():
    current_window = root.focus_get()
    try:
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
    
        rgbTuple = f"{r},{g},{b}"
        
        hex_c = quick_hex(r,g,b)
        current_window.delete("insert linestart", "insert lineend")
        current_window.insert("insert", hex_c)
        show_color()
        output_window.delete(1.0, "1.end")
        output_window.insert(1.0, rgbTuple)
        
    except Exception as e:
        output_window.insert(1.0, f"{e}")

def quick_save():
    current_widget = root.focus_get()
    
    page = current_widget.get("1.0", "end-1c")
    
    with open("last_code.txt", "w") as f:
        f.write(page)
        f.close()
        
    try:
    	with open("qt6_temp.cpp", "w") as tFile:
    		tFile.write(page)
    		tFile.close()
    except:
    	pass



def quick_load():
    current_widget = root.focus_get()
    try:
        with open("last_code.txt", "r") as f:
            current_widget.delete("1.0", "end")
            current_widget.insert("1.0", f.read())
    except FileNotFoundError:
        pass



def remove_empty_lines():
    current_widget = root.focus_get()
    original_position = current_widget.index(tk.INSERT)
    text_content = current_widget.get("1.0", "end")
    non_empty_lines = [line for line in text_content.split("\n") if line.strip()]
    new_text = "\n".join(non_empty_lines)
    current_widget.delete("1.0", "end")
    current_widget.insert("1.0", new_text)

    current_widget.mark_set(tk.INSERT, original_position)
    current_widget.see(tk.INSERT)


def exit_app():
    editor.focus_set()
    quick_save()
    root.after(200, lambda : root.destroy())
    


def list_functions():    
    current_widget = root.focus_get()
    
    def worker():
        try:
            content = current_widget.get("1.0", tk.END)
            lines = content.split("\n")
            functions = []

            for line_num, line in enumerate(lines, start=1):
                line = line.strip()
                if line.startswith("def "):
                    function_name = line.split("(")[0].split("def ")[1]
            
                    functions.append((function_name, line_num))

                elif line.startswith("void "):
                    function_name = line.split("(")[0].split("void ")[1]
                    functions.append((function_name, line_num))
                elif line.startswith("fn "):
                    function_name = line.split("(")[0].split("fn ")[1]
                    functions.append((function_name, line_num))
            

            
                        
            functions.sort(key=lambda x: x[0])  # Sort functions alphabetically by function name
    
            func_amount = len(functions)
            
            extra_window.delete(1.0, "end")
            extra_window.insert(1.0, f"Functions [{func_amount}] : Line\n-----------------------\n\n")

    
            for function_name, line_num in functions:
                extra_window.insert("end", f"{function_name} : {line_num}\n")

        except:
            pass        
    threading.Thread(target=worker).start()    

def go_to_line_selected(event=None):
    current_widget = root.focus_get()
    try:
        if isinstance(current_widget, tk.Text):
            selected_text = current_widget.get(tk.SEL_FIRST, tk.SEL_LAST).strip()
            if selected_text.isdigit() and "," not in selected_text:
                line_number = int(selected_text)
                if line_number > 0:
                    line_index = f"{line_number}.0"
                    editor.mark_set("insert", line_index)
                    editor.focus_set()
                    editor.see(line_index)
                    highlight_code_single()
    except:
        pass



font_size = 12

root = tk.Tk()
root.geometry("1170x630")
root.config(bg="#5e5a29")



editor = tk.Text(
    root,
    wrap="word",
    font=("Hack", font_size),
    undo=True,
    width=56,
    height=14,
    bg="black",
    fg="#e5e5e5",
    padx=6,
    pady=6,
    insertbackground="cyan",
    insertwidth=3,
    bd=3
)

editor.place(
    x=90,
    y=34
)


output_window = tk.Text(
    root,
    wrap="word",
    undo=True,
    font=("Hack", 12),
    bg = "#d8fcb4",
    fg = "#01462a",
    width=46,
    height=10,
    insertwidth=3,
    padx=6,
    pady=6,
    bd=5
)

output_window.place(
    x=90,
    y=390
)


extra_window = tk.Text(
    root,
    wrap="word",
    undo=True,
    width=43,
    height=24,
    font=("Hack", 12),
    bg = "#e5f78c",
    fg = "black",
    insertbackground="black",
    insertwidth=3,
    padx=6,
    pady=6,
    bd=3
)

extra_window.place(
    x=700,
    y=36
)


files_button = tk.Button(
    root,
    text="ls **",
    command=list_files,
    font=("Hack", 10),
    bd=4,
    width=4
)

files_button.place(x=10, y=20)


view_button = tk.Button(
    root,
    text="View",
    command=open_file_from_cursor,
    font=("Hack", 10),
    bd=4,
    width=4
)

view_button.place(x=10, y=60)


open_button = tk.Button(
    root,
    text="Open",
    command=open_file,
    font=("Hack", 10),
    bd=4,
    width=4
)

open_button.place(x=10, y=100)

saveas_button = tk.Button(
    root,
    text="Save As",
    command=save_file,
    font=("Hack", 10),
    bd=4,
    width=4
)

saveas_button.place(x=10, y=140)


save_button = tk.Button(
    root,
    text="Save",
    command=save_last_opened,
    font=("Hack", 10),
    bd=4,
    width=4
)

save_button.place(x=10, y=180)

c_button = tk.Button(
    root,
    text="C >",
    command=run_c,
    font=("Hack", 10),
    bd=4,
    width=4
)

c_button.place(x=10, y=220)

cpp_button = tk.Button(
    root,
    text="C++",
    command=run_cpp,
    font=("Hack", 10),
    bd=4,
    width=4
)

cpp_button.place(x=10, y=260)

rust_button = tk.Button(
    root,
    text="C++/Qt6",
    command=run_cpp_app,
    font=("Hack", 10),
    bd=4,
    width=4
)

rust_button.place(x=10, y=300)

golang_button = tk.Button(
    root,
    text="Rust",
    command=run_rust,
    font=("Hack", 10),
    bd=4,
    width=4
)

golang_button.place(x=10, y=340)


bash_button = tk.Button(
    root,
    text="Bash",
    command=run_bash,
    font=("Hack", 10),
    bd=4,
    width=4
)

bash_button.place(x=10, y=380)


go_button = tk.Button(
    root,
    text="GoLang",
    command=run_golang,
    font=("Hack", 10),
    bd=4,
    width=4
)

go_button.place(x=10, y=420)


python_button = tk.Button(
    root,
    text="Python3",
    command=run_python,
    font=("Hack", 10),
    bd=4,
    width=4
)

python_button.place(x=10, y=460)

js_button = tk.Button(
    root,
    text="JavaScript",
    command=run_javascript,
    font=("Hack", 10),
    bd=4,
    width=4
)

js_button.place(x=10, y=500)


unix_toggle_button = tk.Button(
    root,
    text="Unix",
    command=unix_command,
    font=("Hack", 10),
    bd=4,
    width=4
)

unix_toggle_button.place(x=10, y=540)


unix_toggle_button = tk.Button(
    root,
    text="Unix:On",
    command=toggle_command_mode,
    bg="lightgreen",
    font=("Hack", 10),
    bd=4,
    width=4
)

unix_toggle_button.place(x=10, y=580)


highlight_toggle_button = tk.Button(
    root,
    text="Pygment:On",
    command=toggle_highlight_mode,
    bg="lightgreen",
    font=("Hack", 10),
    bd=4,
    width=6
)

highlight_toggle_button.place(x=85, y=345)


root_button = tk.Button(
    root,
    text="Root",
    command=random_root,
    font=("Hack", 10),
    bd=4,
    width=4
)

root_button.place(x=170, y=345)

pycompile_button = tk.Button(
    root,
    text="PyComp",
    command=check_python,
    font=("Hack", 10),
    bd=4,
    width=4
)

pycompile_button.place(x=240, y=345)

history_button = tk.Button(
    root,
    text="LastCmd",
    command=last_command,
    font=("Hack", 10),    
    bd=4,
    width=4
)

history_button.place(x=310, y=345)

exit_button = tk.Button(
    root,
    text="Exit",
    command=exit_app,
    bg="#440000",
    fg="white",
    font=("Hack", 10),
    bd=4,
    width=4
)

exit_button.place(x=380, y=345)


pymode_button = tk.Button(
    root,
    text="PMode: Off",
    command=toggle_pymode,
    font=("Hack", 10),
    bd=4,
    width=7
)

pymode_button.place(x=450, y=345)


light_screen_button = tk.Button(
    root,
    text="light",
    command=random_light_screen,
    font=("Hack", 10),
    bd=4,
    width=3
)

light_screen_button.place(x=544, y=345)


cutup_button = tk.Button(
    root,
    text="CutUp",
    command=cut_above,
    font=("Hack", 10),
    bd=4,
    width=3
)

cutup_button.place(x=610, y=345)

cutDown_button = tk.Button(
    root,
    text="CutDown",
    command=cut_below,
    font=("Hack", 10),
    bd=4,
    width=3
)

cutDown_button.place(x=610, y=385)


style_button = tk.Button(
    root,
    text="1/Screen",
    command=invert_screen,
    font=("Hack", 10),
    bd=4,
    width=3
)

style_button.place(x=610, y=425)

lastfile_button = tk.Button(
    root,
    text="File?",
    command=show_last_file,
    font=("Hack", 10),
    bd=4,
    width=3
)

lastfile_button.place(x=610, y=465)


pythonPartial_button = tk.Button(
    root,
    text="PyPartial",
    command=run_python_partial,
    font=("Hack", 10),
    bd=4,
    width=5
)

pythonPartial_button.place(x=630, y=535)


line_button = tk.Button(
    root,
    text="Line",
    command=go_to_line,
    font=("Hack", 10),
    bd=4,
    width=5
)

line_button.place(x=710, y=535)

rgb_button = tk.Button(
    root,
    text="rgbToHex",
    command=tuple_to_hex,
    font=("Hack", 10),
    bd=4,
    width=5
)

rgb_button.place(x=790, y=535)

num_button = tk.Button(
    root,
    text="NumToHex",
    command=numToHex,
    font=("Hack", 10),
    bd=4,
    width=5
)

num_button.place(x=870, y=535)


hex_button = tk.Button(
    root,
    text="HexToNum",
    command=hexToNum,
    font=("Hack", 10),
    bd=4,
    width=5
)

hex_button.place(x=950, y=535)


show_color_button = tk.Button(
    root,
    text="ShowHexC",
    command=show_color,
    bd=4,
    font=("Hack", 10),
    width=5
)

show_color_button.place(x=1030, y=535)

get_colors_button = tk.Button(
    root,
    text="getColrs",
    command=get_colors,
    font=("Hack", 10),
    bd=4,
    width=5
)

get_colors_button.place(x=630, y=575)

r_tuple_button = tk.Button(
    root,
    text="RTuple",
    command=random_tuple,
    font=("Hack", 10),
    bd=4,
    width=5
)

r_tuple_button.place(x=710, y=575)

eval_button = tk.Button(
    root,
    text="=",
    command=eval_exp,
    font=("Hack", 10),
    bd=4,
    width=5
)

eval_button.place(x=790, y=575)


qsave_button = tk.Button(
    root,
    text="QSave",
    command=quick_save,
    font=("Hack", 10),
    bd=4,
    width=5
)

qsave_button.place(x=870, y=575)

qload_button = tk.Button(
    root,
    text="QLoad",
    command=quick_load,
    font=("Hack", 10),
    bd=4,
    width=5
)

qload_button.place(x=950, y=575)

pyFunc_button = tk.Button(
    root,
    text="PyFunc",
    command=list_functions,
    font=("Hack", 10),
    bd=4,
    width=5
)

pyFunc_button.place(x=1030, y=575)



editor.bind("<Control-r>", run_python)
editor.bind("<Control-v>", open_file_from_cursor)
editor.bind("<Control-o>", open_file)
editor.bind("<Control-s>", save_last_opened)
editor.bind("<Control-u>", undo_last)
editor.bind("<Control-k>", clear_window)
editor.bind("<KeyRelease>", update_data)
editor.bind("<Return>", auto_indent)
editor.bind("<Control-q>", exit_app)

extra_window.bind("<<Selection>>", go_to_line_selected)

output_window.bind("<Control-q>", exit_app)

extra_window.bind("<Control-r>", run_python)
extra_window.bind("<Control-v>", open_file_from_cursor)
extra_window.bind("<Control-o>", open_file)
extra_window.bind("<Control-s>", save_last_opened)
extra_window.bind("<Control-u>", undo_last)
extra_window.bind("<Control-k>", clear_window)
extra_window.bind("<Control-q>", lambda x : root.destroy())

extra_window.bind("<Return>", detect_command)



root.mainloop()

