import asyncio
import keyword
import os
import random
import readline
import re
import shutil
import subprocess
import tempfile
import threading
from time import sleep

from prompt_toolkit import Application, PromptSession
from prompt_toolkit.application import run_in_terminal
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.enums import EditingMode
from prompt_toolkit.history import FileHistory
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import HSplit, VSplit, Layout
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style
from prompt_toolkit.styles.pygments import style_from_pygments_cls
from prompt_toolkit.widgets import (
    Button,
    Dialog,
    Frame,
    Label,
    TextArea,
)

from pygments.lexers import (
    NasmLexer,
    BashLexer,
    CLexer,
    CppLexer,
    CssLexer,
    GoLexer,
    HtmlLexer,
    JavascriptLexer,
    PythonLexer,
    RustLexer,
)
from pygments.styles import get_style_by_name

all_themes = [
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


CYAN = "\033[1;38;2;100;255;255m"
BLUE = "\033[1;38;2;110;110;255m"
GREY = "\033[1;38;2;210;210;210m"
GREEN = "\033[1;38;2;100;255;100m"
ORANGE = "\033[1;38;2;255;165;0m"
RESET = "\033[0m"

BLUE_BACK = "\033[1;48;2;0;0;50m"

floats = []


file_buffers = {}
open_files = []
file_index = 0
current_file = "untitled.py"


history_file = os.path.expanduser("~/.js_shell_history")


session = PromptSession(
    auto_suggest=AutoSuggestFromHistory(),
    history=FileHistory(history_file)
)


os.system("clear")

file_name = session.prompt([(f"class: orange bold", "File: ")]).strip()



if not os.path.exists(file_name):
    os.system(f"touch {file_name}")


if not file_name or not file_name.isascii():
    file_name = ".last_file_content"


newFile = ""


pygments_on = True


try:
    with open(file_name, "r") as f:
        current_text = f.read()
except FileNotFoundError:
    current_text = ""


def get_lexer():
    if not pygments_on:
        return None
    elif file_name.endswith(".asm"):
        return PygmentsLexer(NasmLexer)
    elif file_name.endswith(".sh"):
        return PygmentsLexer(BashLexer)
    elif file_name.endswith(".c"):
        return PygmentsLexer(CLexer)
    elif file_name.endswith(".cpp"):
        return PygmentsLexer(CppLexer)
    elif file_name.endswith(".rs"):
        return PygmentsLexer(RustLexer)
    elif file_name.endswith(".go"):
        return PygmentsLexer(GoLexer)
    elif file_name.endswith(".py"):
        return PygmentsLexer(PythonLexer)
    elif file_name.endswith(".js"):
        return PygmentsLexer(JavascriptLexer)
    else:
        return PygmentsLexer(PythonLexer)


def get_theme_style():
    if file_name.endswith(".c") or file_name.endswith(".asm"):
        return style_from_pygments_cls(get_style_by_name("lightbulb"))    
    if file_name.endswith(".c") or file_name.endswith(".cpp"):
        return style_from_pygments_cls(get_style_by_name("lightbulb"))
    elif file_name.endswith(".rs"):
        return style_from_pygments_cls(get_style_by_name("github-dark"))
    elif file_name.endswith(".sh"):
        return style_from_pygments_cls(get_style_by_name("coffee"))
    elif file_name.endswith(".go"):
        return style_from_pygments_cls(get_style_by_name("zenburn"))
    elif file_name.endswith(".py"):
        return style_from_pygments_cls(get_style_by_name("paraiso-dark"))
    else:
        return style_from_pygments_cls(get_style_by_name("one-dark"))


pygment_style = get_theme_style()



style = Style(
    [
        *pygment_style.style_rules,
        ("status-bar", "bg:#222222 fg:orange bold"),
        ("theme-editor", "bg:black fg:white"),
        ("theme-output_window", "bg:gold fg:black bold"),
    ]
)


editor = TextArea(
    text=current_text,
    style="class:theme-editor",
    lexer=get_lexer(),
    scrollbar=True,
    width=20,
    height=16,
    line_numbers=True,
    multiline=True,
    wrap_lines=True,
    focus_on_click=True,
)


output_window = TextArea(
    text="",
    style="class:theme-output_window",
    #lexer=PygmentsLexer(PythonLexer),
    width=20,
    height=12,
    multiline=True,
    wrap_lines=True,
    focus_on_click=True,
)


status_bar = Label(
    text="File: None",
    style="class:status-bar",
)


root_container = HSplit([
    HSplit([
        editor,
        status_bar,
        output_window
    ])
])


home_files = os.listdir(".")

keywords = [
    "#include",
    "<iostream>",
    "Boolean(",
    "False",
    "None",
    "Println",
    "Symbol",
    "True",
    "assert",
    "async",
    "await",
    "break",
    "capitalize",
    "case",
    "casefold",
    "center",
    "class",
    "console",
    "const",
    "continue",
    "count",
    "default",
    "dict",
    "document",
    "elif",
    "else",
    "encode",
    "endswith",
    "enumerate",
    "except",
    "expandtabs",
    "export",
    "extends",
    "false",
    "finally",
    "find",
    "float",
    "fmt",
    "format",
    "format_map",
    "from",
    "func",
    "func",
    "function",
    "global",
    "import",
    "index",
    "input(",
    "instanceof()",
    "isalnum()",
    "isalpha()",
    "isascii()",
    "isdecimal()",
    "isdigit()",
    "isidentifier()",
    "islower()",
    "isnumeric()",
    "isprintable()",
    "isspace()",
    "istitle()",
    "isupper()",
    "join()",
    "lambda",
    "list()",
    "ljust()",
    "lower()",
    "lstrip()",
    "main",
    "maketrans",
    "match()",
    "namespace",
    "nonlocal",
    "null",
    "open()",
    "partition",
    "pass",
    "print(",
    "raise",
    "range(",
    "removeprefix()",
    "removesuffix()",
    "replace(",
    "return",
    "rfind(",
    "rindex(",
    "rjust(",
    "rpartition",
    "rsplit()",
    "rstrip()",
    "split()",
    "splitlines()",
    "startswith(",
    "static",
    "strip()",
    "super",
    "swapcase",
    "switch",
    "this",
    "title",
    "translate",
    "true",
    "tuple",
    "typeof",
    "undefined",
    "upper",
    "while",
    "window",
    "with",
    "yield",
    "zfill(",
    "matplot.pyplot",
    "prompt_toolkit",
    "random",
    "tkinter",
    "numpy",
    "scipy",
]


def auto_complete(event):
    editor = event.current_buffer
    word = editor.document.get_word_before_cursor(WORD=True)

    if not word:
        return

    matches = [item for item in keywords + os.listdir(".") if item.startswith(word)]

    if matches:
        completion = matches[0][len(word) :]
        editor.insert_text(completion)


def get_language():
    if file_name.startswith("."):
        return "'Hidden' file"
    if file_name.endswith(".txt"):
        return "Text"
    if file_name.endswith(".c"):
        return "C"
    elif file_name.endswith(".cpp"):
        return "C++"
    elif file_name.endswith(".rs"):
        return "Rust"
    if file_name.endswith(".sh"):
        return "Bash"
    if file_name.endswith(".go"):
        return "Golang"
    if file_name.endswith(".py"):
        return "Python"
    if file_name.endswith(".js"):
        return "JavaScript"
    else:
        return ""


def update_status_bar(message=None):
    if message:
        status_bar.text = message
    else:
        try:

            ln = editor.buffer.document.cursor_position_row + 1
            col = editor.buffer.document.cursor_position_col + 1
        except:
            ln, col = 1, 1
        status_bar.text = f"File: '{file_name}' |  {ln}, {col}  |  {get_language()} "


def on_editor_change(_):
    update_status_bar()


editor.buffer.on_cursor_position_changed += on_editor_change
editor.buffer.on_text_changed += on_editor_change


async def show_temp_message(msg, delay=2):
    update_status_bar(msg)
    await asyncio.sleep(delay)
    update_status_bar()


current_widget = editor

# Key bindings
kb = KeyBindings()


@kb.add("c-right")
def quick_command(event):
    def run_cmd():
        global current_widget

        current_line_text = current_widget.document.current_line
        cmd = current_line_text

        try:
            sub_cmd = subprocess.run([cmd], capture_output=True, text=True, shell=True)

            if sub_cmd.returncode != 0:
                current_widget.buffer.insert_text(f"\n\n{sub_cmd.stderr}\n")
            else:
                current_widget.buffer.insert_text(f"\n\n{sub_cmd.stdout}\n")
        except:
            event.app.layout.focus(editor)
            current_widget = editor
            pass

    run_cmd()



word_index = 0

saved_words = []


@kb.add("s-down")
def save_word(event=None):

    word = editor.document.get_word_before_cursor()

    if len(saved_words) > 20:
        saved_words.pop(0)
    if len(word) > 3:
        saved_words.append(word)


@kb.add("s-up")
def last_word(event):
    global word_index

    try:
        word_index -= 1

        if word_index < -(len(saved_words)):
            word_index = -1

        output_window.text = f"{saved_words[word_index]}"
    except:
        pass


@kb.add("s-right")
def insert_word(event):
    try:
        editor.buffer.insert_text(f"{saved_words[word_index]}")
    except:
        pass


@kb.add("c-b")
def quick_bash(event):
    def run_subprocess():
        os.system("python3 ~/quick_bash.py")
    """
        os.system("clear")
        sleep(0.3)

        while 1:

            cmd = input(f"{GREEN}@ {RESET}").strip()

            if cmd == "q" or cmd == "exit":
                return
            os.system(cmd)
    """
    run_in_terminal(run_subprocess)


@kb.add("c-y")
def reload_file(event):
    with open(file_name, "r") as f:
        editor.text = f.read()
        f.close()
    status_bar.text = ""
    status_bar.text = f"File: {file_name} Reloaded"


@kb.add("c-s")
def save_file(event):
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(editor.text)
    status_bar.text = f"File: {file_name} saved ✓"

    def clear_bar():
        sleep(1)
        status_bar.text = f"File: {file_name}"

    threading.Thread(target=clear_bar, daemon=True).start()


@kb.add("c-g")
def search_from_cursor(event):
    def do_search():
        os.system("clear")
        sleep(0.3)
        search_input = input("\nFind: ").strip()

        term = search_input
        if not term:
            floats.clear()
            event.app.layout.focus(editor)
            return

        buf = editor.buffer
        start = buf.cursor_position
        found_index = buf.document.text.find(term, start)
        if found_index != -1:
            buf.cursor_position = found_index
            buf.selection_state = None

        event.app.layout.focus(editor)

    run_in_terminal(do_search)


@kb.add("c-l")
def goto_line(event):

    sleep(0.3)

    def jump():
        os.system("clear")
        try:
            line = input(f"\nLine: ").strip()
            line_number = int(line)
            lines = editor.text.splitlines()
            if 1 <= line_number <= len(lines):
                pos = sum(len(l) + 1 for l in lines[: line_number - 1])
                editor.buffer.cursor_position = pos
        except:
            pass

    run_in_terminal(jump)


@kb.add("c-down")
def go_down(event):
    global current_widget

    try:
        event.app.layout.focus(output_window)
        current_widget = output_window
    except Exception as e:
        output_window.text = e


@kb.add("c-up")
def go_down(event):
    global current_widget

    try:
        event.app.layout.focus(editor)
        current_widget = editor
    except Exception as e:
        output_window.text = e


@kb.add("c-k")
def clear_all(event):
    global file_name
    
    editor.text = ""
    output_window.text = ""
    file_name = 'Untitled'

@kb.add("c-z")
def save_as_file(event):
    def save_as():
        global file_name
        
        os.system("clear")
        sleep(0.3)

        file = input("\nSave As: ").strip()

        with open(file, "w", encoding="utf-8") as f:
            f.write(editor.text)
            status_bar.text = f"File Saved As: {file} ✓"
        file_name = file
        def clear_bar():
            sleep(1)
            status_bar.text = f"File: {file}"

        threading.Thread(target=clear_bar, daemon=True).start()

    run_in_terminal(save_as)





@kb.add("c-p")
def run_code_quicj(event):
    global file_name

    try:
        code = editor.text

        ext = os.path.splitext(file_name)[1]

        with tempfile.NamedTemporaryFile("w", delete=False, suffix=ext) as tmp:
            tmp.write(code)
            tmp_filename = tmp.name

        if ext == ".c":
            cmd = f"gcc {tmp_filename} && ./a.out"
        elif ext == ".cpp":
            cmd = f"g++ {tmp_filename} && ./a.out"
        elif ext == ".go":
            cmd = f"go run {tmp_filename}"
        elif ext == ".py":
            cmd = f"python3 {tmp_filename}"
        elif ext == ".sh":
            cmd = f"bash {tmp_filename}"
        elif ext == ".js":
            cmd = f"node {tmp_filename}"
        elif ext in (".asm", ".s"):
            object_file = tmp_filename.removesuffix(ext) + ".o"
            executable_file = tmp_filename.removesuffix(ext)

            assemble = subprocess.run(
                ["nasm", "-f", "elf64", tmp_filename, "-o", object_file],
                capture_output=True,
                text=True
            )

            if assemble.returncode != 0:
                output_window.text = assemble.stderr
                return

            link = subprocess.run(
                ["ld", object_file, "-o", executable_file],
                capture_output=True,
                text=True
            )

            if link.returncode != 0:
                output_window.text = link.stderr
                return

            exe = subprocess.run(
                [executable_file],
                capture_output=True,
                text=True
            )

            if exe.returncode != 0:
                output_window.text = exe.stderr
            else:
                output_window.text = exe.stdout

            return
        else:
            return

        if "cin >>" in code or "input(" in code or "read -p" in code:
            output_window.text = "\nCan't run this code without run_in_terminal()\n\nTry: pressing Control + r instead.\n\n  You can also use quick bash by\n  pressing Control + b."

        else:
            runCode = subprocess.run(
                [cmd],
                capture_output=True,
                text=True,
                shell=True
            )

            if runCode.returncode != 0:
                output_window.text = runCode.stderr
            else:
                output_window.text = runCode.stdout

    except Exception as e:
        output_window.text = str(e)




@kb.add("c-c")
def toggle_syntax(event):
    global pygments_on
    pygments_on = not pygments_on
    editor.lexer = get_lexer() if pygments_on else None
    event.app.invalidate()


@kb.add("tab")
def insert_indent(event):
    editor.buffer.insert_text("    ")


@kb.add("c-space")
def complete_(event):
    auto_complete(event)


@kb.add("c-f")
def new_file(event):
    def open_file():
        global file_name
        global style

        os.system("clear")

        file = input("\nFile: ").strip()
        if not file:
            file = file_name

        if os.path.exists(file):
            with open(file, "r", encoding="utf-8") as f:
                editor.text = ""
                editor.text = f.read()
                f.close()
                file_name = file
        else:
            os.system(f"touch {file}")

            with open(file, "r") as f:
                editor.text = ""
                editor.text = f.read()
                f.close()
                file_name = file

        pygment_style = get_theme_style()

        editor.lexer = get_lexer()
        editor.style = get_theme_style()
        event.app.invalidate()

        status_bar.text = f"File: {file_name}"

    run_in_terminal(open_file)


@kb.add("c-o")
def view_file_from_cursor(event):
    def open_file():
        global file_name
        global style

        os.system("clear")

        try:
            file = editor.document.current_line

            with open(file, "r", encoding="utf-8") as f:
                editor.text = ""
                editor.text = f.read()
                f.close()
                file_name = file

            editor.lexer = get_lexer()
            pygment_style = get_theme_style()
            editor.style = get_theme_style()
            event.app.invalidate()


        except:
            pass

        status_bar.text = f"File: {file_name}"

    run_in_terminal(open_file)


@kb.add("c-t")
def open_shell(event):
    def shell():
        subprocess.run("./q_shell", check=True)

    run_in_terminal(shell)


@kb.add("c-r")
def run_code(event):
    def run_script():
        os.system("clear")
        code = editor.text
        ext = os.path.splitext(file_name)[1]

        with tempfile.NamedTemporaryFile("w", delete=False, suffix=ext) as tmp:
            tmp.write(code)
            tmp_filename = tmp.name

        try:
            if ext == ".py":
                os.system(f"python {tmp_filename}")
            elif ext == ".js":
                os.system(f"node {tmp_filename}")
            elif ext == ".go":
                os.system(f"go run '{tmp_filename}'")
            elif ext == ".c" or ext == ".cpp" or ext == ".rs":
                bin_path = f"{tmp_filename}.bin"
                if ext == ".c":
                    compiler = "gcc"
                elif ext == ".cpp":
                    compiler = "g++"
                else:
                    compiler = "rustc"

                os.system(f"{compiler} {tmp_filename} -o {bin_path} && {bin_path}")
                if os.path.exists(bin_path):
                    os.remove(bin_path)
            else:
                os.system(f"bash {tmp_filename}")

        finally:
            os.remove(tmp_filename)

        sleep(0.5)
        input(f"{ORANGE}\n\n\n( Press Enter to return to editor ){RESET}\n\n")

    run_in_terminal(run_script)


@kb.add("c-d")
def runCppQt6(event):
    def run_qt6():
        os.system("clear")
        code = editor.text
        ext = ".cpp"

        with tempfile.NamedTemporaryFile("w", delete=False, suffix=ext) as tmp:
            tmp.write(code)

            tmp_filename = tmp.name
            eFile = str(tmp_filename.split("/")[-1]).replace(".cpp", ".out")

        try:
            os.system(
                f"g++ {tmp_filename} -o {eFile} $(pkg-config --cflags --libs Qt6Widgets) -lqtermwidget6 && ./{eFile}"
            )

        finally:
            os.remove(tmp_filename)

        sleep(0.5)
        input(f"{ORANGE}\n\n\n( Press Enter to return to editor ){RESET}\n\n")

    run_in_terminal(run_qt6)


@kb.add("c-q")
def _(event):

    with open(".last_file_content", "w", encoding="utf-8") as f:
        f.write(editor.text)
        f.close()

    event.app.exit()


layout = Layout(root_container, focused_element=editor)


app = Application(
    layout=layout,
    style=style,
    full_screen=True,
    mouse_support=True,
    editing_mode=EditingMode.VI,
    key_bindings=kb,
)


app.run()





"""

Key Bindings Guide

Control keys in alphabetical order:
- ctrl + b - quick bash shell
- ctrl + c - toggle syntax highlighting
- ctrl + d - run C++ Qt6 app
- ctrl + f - open or create a new file
- ctrl + g - search/find text from cursor position
- ctrl + k - clear editor and output window
- ctrl + l - jump to a specific line number
- ctrl + o - open a file from the current line
- ctrl + p - run code quickly
- ctrl + q - quit the editor
- ctrl + r - run code in terminal
- ctrl + s - save current file
- ctrl + space - auto-complete
- ctrl + t - open shell
- ctrl + up - focus the editor
- ctrl + down - focus the output window
- ctrl + right - run current line as shell command
- ctrl + y - reload file
- ctrl + z - save file as

Other keys:
- shift + down - save current word to history
- shift + up - move through saved words
- shift + right - insert saved word
- tab - insert 4 spaces

Notes:
- This editor uses VI-style editing mode.
- The status bar shows the current file, cursor position, and detected language.
- Ctrl + r is best for programs that need user input.
- Ctrl + p is best for simple output-only programs.

"""

