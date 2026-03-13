"""Editor designed for developers"""

import os
import re
import tempfile
import threading
import shutil
import subprocess
import asyncio
import readline
from time import sleep
import random
from prompt_toolkit.completion import WordCompleter, Completer, Completion
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit import PromptSession
from prompt_toolkit.application import run_in_terminal
from prompt_toolkit import Application
from prompt_toolkit.layout import Layout, HSplit, VSplit
from prompt_toolkit.layout.containers import FloatContainer, Float
from prompt_toolkit.layout.dimension import Dimension
from prompt_toolkit.widgets import TextArea, Frame, Dialog, Button
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style, merge_styles
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers import (
    BashLexer,
    CLexer,
    RustLexer,
    CppLexer,
    GoLexer,
    PythonLexer,
    HtmlLexer,
    JavascriptLexer,
    CssLexer,
)


from pygments.styles import get_style_by_name
from prompt_toolkit.styles.pygments import style_from_pygments_cls

# -----------------------
# Global variables
# -----------------------
file_buffers = {}
open_files = []
file_index = 0
current_file = "untitled.py"
floats = []
syntax_enabled = True

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

my_themes = [
    "coffee",
    "dracula",
    "github-dark",
    "gruvbox-dark",
    "lightbulb",
    "material",
    "nord-darker",
    "paraiso-dark",
    "zenburn",
]


key_guide = """
Control a : Go to beginning of the line
Control b : Open shell
Control c : Toggle syntax highlighting
Control d : Format pylint output
Control e : Go to the end of the line
Control f : Open file
Control g : Search from cursor
Control w : Print Key Guide
Control k : Clear from cursor to end of line
Control l : Go to line number
Control n : Save As / New file
Control o : Open new page / vertical tab below current
Control p : List functions
Control q : Quit application
Control r : Run code (active editor / bottom editor)
Control s : Save current file
Control t : Run code (top editor)
Control u : Refresh current file #override
Control v : Run pylint on top editor
Control x : Cycle themes
Control y : Close current file
Control z : Cycle open files
Control _ : Clear active editor
Control space : Insert indent
"""

current_theme_index = 3

WHITE = "\033[1;37m"
YELLOW = "\033[1;33m"
CYAN = "\033[1;36m"
LIGHT_BLUE = "\033[1;38;2;150;150;255m"
RED = "\033[1;31m"
GREEN = "\033[1;32m"
RESET = "\033[0m"


# -----------------------
# Utilities
# -----------------------
def load_file(path):
    try:
        with open(path, "r") as f:
            return f.read()
    except:
        return ""


def save_file(path, content):
    with open(path, "w") as f:
        f.write(content)


# -----------------------
# Styles
# -----------------------
base_style = Style.from_dict(
    {
        "top-pane": "bg:black white bold",
        "bottom-pane": "bg:black orange bold",
        "status": "bg:#222255 white bold",
    }
)


def get_lexer():
    if not syntax_enabled:
        return None
    if current_file.endswith(".sh"):
        return PygmentsLexer(BashLexer)
    if current_file.endswith(".c"):
        return PygmentsLexer(CLexer)
    if current_file.endswith(".cpp"):
        return PygmentsLexer(CppLexer)
    if current_file.endswith(".py"):
        return PygmentsLexer(PythonLexer)
    if current_file.endswith(".rs"):
        return PygmentsLexer(RustLexer)
    if current_file.endswith(".go"):
        return PygmentsLexer(GoLexer)
    if current_file.endswith(".html"):
        return PygmentsLexer(HtmlLexer)
    if current_file.endswith(".js"):
        return PygmentsLexer(JavascriptLexer)
    else:
        return None


last_cursor_pos = {}


def editor(filename="untitled.py"):

    editor = TextArea(
        text="",
        lexer=get_lexer(),
        scrollbar=False,
        line_numbers=False,
        focus_on_click=True,
        wrap_lines=True,
        multiline=True,
        height=Dimension(min=9),
    )

    status_bar = TextArea(
        text="",
        height=1,
        style="class:status",
        multiline=False,
        focusable=False,
    )

    def update_status_bar(message=None):
        if message:
            status_bar.text = message
        else:
            try:
                ln = editor.buffer.document.cursor_position_row + 1
                col = editor.buffer.document.cursor_position_col + 1
            except:
                ln, col = 1, 1
            status_bar.text = f"'{current_file}':     {ln}, {col}"

    def on_editor_change(_):
        update_status_bar()

    editor.buffer.on_cursor_position_changed += on_editor_change
    editor.buffer.on_text_changed += on_editor_change

    async def show_temp_message(msg, delay=2):
        update_status_bar(msg)
        await asyncio.sleep(delay)
        update_status_bar()

    def get_theme_style():
        if filename.endswith(".sh"):
            return style_from_pygments_cls(get_style_by_name("gruvbox-dark"))
        elif (
            filename.endswith(".c")
            or filename.endswith(".cpp")
            or filename.endswith(".go")
        ):
            return style_from_pygments_cls(get_style_by_name("lightbulb"))
        elif filename.endswith(".py"):
            return style_from_pygments_cls(get_style_by_name("material"))
        elif (
            filename.endswith(".js")
            or filename.endswith(".html")
            or filename.endswith(".rs")
        ):
            return style_from_pygments_cls(get_style_by_name("github-dark"))
        else:
            return None

    style = merge_styles([get_theme_style(), base_style])

    kb = KeyBindings()

    @kb.add("c-u")
    def reload_current_file(event):
        if current_file:
            file_buffers[current_file] = editor.text
            editor.text = load_file(current_file)
            editor.lexer = get_lexer()
            event.app.layout.focus(editor)

    @kb.add("c-x")
    def cycle_themes(event):
        global current_theme_index, style
        current_theme_index = (current_theme_index + 1) % len(my_themes)
        style = merge_styles(
            [
                style_from_pygments_cls(
                    get_style_by_name(my_themes[current_theme_index])
                ),
                base_style,
            ]
        )
        editor.lexer = get_lexer()
        event.app.style = style
        update_status_bar(f"Theme: {all_themes[current_theme_index]}")

    @kb.add("c-c")
    def toggle_syntax(event):
        global syntax_enabled
        syntax_enabled = not syntax_enabled
        editor.lexer = get_lexer() if syntax_enabled else None
        event.app.invalidate()

    @kb.add("c-space")
    def insert_indent(event):
        editor.buffer.insert_text("    ")

    @kb.add("c-q")
    def quit_app(event):
        for filename in os.listdir("."):
            if os.path.isfile(filename) and "tmp" in filename:
                os.remove(filename)
        event.app.exit()

    @kb.add("c-y")
    def close_current_file(event):
        if not open_files:
            return

        def confirm_close():
            if len(open_files) <= 1:
                event.app.exit()
                return
            global current_file, file_index
            open_files.pop(file_index)
            file_index %= len(open_files)
            current_file = open_files[file_index]
            editor.text = load_file(current_file)
            floats.clear()
            event.app.layout.focus(editor)
            update_status_bar()

        def cancel_close():
            floats.clear()
            event.app.layout.focus(editor)

        dialog = Dialog(
            title="Close File",
            body=TextArea(
                text=f"Close '{current_file}' ??",
                height=1,
                multiline=False,
                focusable=False,
            ),
            buttons=[
                Button(text="Yes", handler=confirm_close),
                Button(text="Cancel", handler=cancel_close),
            ],
            width=50,
            modal=True,
        )

        floats.clear()
        floats.append(Float(content=dialog))
        event.app.layout.focus(dialog)

    @kb.add("c-s")
    def save_current(event):
        if current_file:
            file_buffers[current_file] = editor.text
            save_file(current_file, editor.text)
            asyncio.ensure_future(
                show_temp_message(f"File: '{current_file}' Saved.", 2)
            )

    @kb.add("c-n")
    def save_as_dialog(event):
        filename_input = TextArea(height=1, multiline=False)

        def save_handler():
            global current_file, file_index
            path = filename_input.text.strip()
            if not path:
                return
            with open(path, "w") as f:
                f.write(editor.text)
            if current_file:
                file_buffers[current_file] = editor.text
            if path not in open_files:
                open_files.append(path)
            file_index = open_files.index(path)
            current_file = path
            editor.text = load_file(path)
            editor.lexer = get_lexer()
            floats.clear()
            event.app.layout.focus(editor)
            update_status_bar(f"Saved As: {current_file}")

        def cancel():
            floats.clear()
            event.app.layout.focus(editor)
            update_status_bar()

        dialog = Dialog(
            title="Save As",
            body=filename_input,
            buttons=[
                Button(text="Save", handler=save_handler),
                Button(text="Cancel", handler=cancel),
            ],
            width=60,
            modal=True,
        )

        floats.clear()
        floats.append(Float(content=dialog))
        event.app.layout.focus(filename_input)

    @kb.add("c-_")
    def clear_active(event):
        if event.app.layout.has_focus(editor):
            editor.text = ""
        elif event.app.layout.has_focus(bottom_editor):
            bottom_editor.text = ""
        update_status_bar()

    @kb.add("c-b")
    def open_shell(event):
        def shell():
            subprocess.run("bash", check=True)

        run_in_terminal(shell)

    @kb.add("c-r")
    def run_code(event):
        def run_script():
            os.system("clear")
            code = editor.text
            ext = os.path.splitext(current_file)[1]

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

            sleep(1)
            input(f"\n\n\n{LIGHT_BLUE}( Press Enter to return to editor ){RESET}\n\n")

        run_in_terminal(run_script)

    @kb.add("c-f")
    def open_file_dialog(event):
        filename_input = TextArea(height=1, multiline=False)

        def open_handler():
            global current_file, file_index
            path = filename_input.text.strip()
            if not path:
                return
            if not os.path.exists(path):
                open(path, "w").close()
            if current_file:
                file_buffers[current_file] = editor.text
            if path not in open_files:
                open_files.append(path)
            file_index = open_files.index(path)
            current_file = path
            editor.text = load_file(path)
            editor.lexer = get_lexer()
            floats.clear()
            event.app.layout.focus(editor)
            update_status_bar()

        def cancel():
            floats.clear()
            event.app.layout.focus(editor)
            update_status_bar()

        dialog = Dialog(
            title="Open File",
            body=filename_input,
            buttons=[
                Button(text="Open", handler=open_handler),
                Button(text="Cancel", handler=cancel),
            ],
            width=60,
            modal=True,
        )

        floats.clear()
        floats.append(Float(content=dialog))
        event.app.layout.focus(filename_input)

    @kb.add("c-z")
    def cycle_files(event):
        global file_index, current_file, last_cursor_pos
        if not open_files:
            return
        last_cursor_pos[current_file] = editor.buffer.cursor_position
        file_buffers[current_file] = editor.text
        file_index = (file_index + 1) % len(open_files)
        current_file = open_files[file_index]
        editor.text = file_buffers.get(current_file, "")
        editor.buffer.cursor_position = last_cursor_pos.get(current_file, 0)
        update_status_bar()

    @kb.add("c-l")
    def goto_line_dialog(event):
        line_input = TextArea(height=1, multiline=False, prompt="Line #: ")

        def jump():
            try:
                line_number = int(line_input.text.strip())
                lines = editor.text.splitlines()
                if 1 <= line_number <= len(lines):
                    pos = sum(len(l) + 1 for l in lines[: line_number - 1])
                    editor.buffer.cursor_position = pos
            except:
                pass
            floats.clear()
            event.app.layout.focus(editor)

        def cancel():
            floats.clear()
            event.app.layout.focus(editor)

        dialog = Dialog(
            title="Go To Line",
            body=line_input,
            buttons=[
                Button(text="Go", handler=jump),
                Button(text="Cancel", handler=cancel),
            ],
            width=40,
            modal=True,
        )

        floats.clear()
        floats.append(Float(content=dialog))
        event.app.layout.focus(line_input)

    @kb.add("c-g")
    def search_from_cursor(event):
        search_input = TextArea(height=1, multiline=False)

        def do_search():
            term = search_input.text.strip()
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
            floats.clear()
            event.app.layout.focus(editor)

        def cancel():
            floats.clear()
            event.app.layout.focus(editor)

        dialog = Dialog(
            title="Search",
            body=search_input,
            buttons=[
                Button(text="Find", handler=do_search),
                Button(text="Cancel", handler=cancel),
            ],
            width=60,
            modal=True,
        )

        floats.clear()
        floats.append(Float(content=dialog))
        event.app.layout.focus(search_input)

    root_container = FloatContainer(
        content=HSplit(
            [
                editor,
                status_bar,
            ]
        ),
        floats=floats,
    )

    global current_file, file_index

    if not os.path.exists(filename):
        open(filename, "w").close()

    current_file = filename
    open_files.append(filename)
    file_index = 0
    editor.text = load_file(filename)
    update_status_bar()

    app = Application(
        layout=Layout(root_container),
        key_bindings=kb,
        full_screen=True,
        mouse_support=True,
        style=style,
    )

    app.run()


class PathCompleter(Completer):
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor.strip()
        if not text:
            return
        parts = text.split()
        last = parts[-1] if parts else ""
        dirname, prefix = os.path.split(last)
        dirname = dirname or "."
        try:
            for name in os.listdir(dirname):
                if name.startswith(prefix):
                    path = os.path.join(dirname, name)
                    display = name + ("/" if os.path.isdir(path) else "")
                    yield Completion(display, start_position=-len(prefix))
        except Exception:
            pass


HOME_DIR = "/root/"
history_file = os.path.expanduser("~/.my_prompt_history")

session = PromptSession(
    auto_suggest=AutoSuggestFromHistory(),
    history=FileHistory(history_file),
    completer=PathCompleter(),
)


while True:
    prompt_label = "\n$ "
    try:
        colors = [
            "cyan",
            "yellow",
            "orange",
            "lightblue",
            "lightgrey",
        ]
        prompt_color = random.choice(colors)
        command = session.prompt([(f"class:{prompt_color} bold", prompt_label)]).strip()
        os.system(command)

        if not command:
            continue

        if command.startswith("edit "):
            file = command[5:]
            editor(file)

        elif command == "cd":
            os.chdir(HOME_DIR)
            os.system("pwd")

        elif command.startswith("cd"):
            new_path = command[2:].strip()
            if new_path in ("", "~", "~/"):
                new_path = HOME_DIR
            else:
                if new_path.startswith("~/"):
                    new_path = new_path.replace("~", HOME_DIR, 1)
                new_path = os.path.abspath(os.path.expanduser(new_path))
            os.chdir(new_path)
            os.system("pwd")

        if command == "l":
            os.system("ls")

        if command == "k":
            os.system("clear")
        if command.lower() == "q":
            break
    except Exception as e:
        print(e)
