import asyncio
import subprocess
import tempfile
from pathlib import Path
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, Float, FloatContainer, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.widgets import TextArea, Frame, Dialog, Button
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers import PythonLexer, JavascriptLexer, HtmlLexer, BashLexer, JavaLexer
from pygments.styles import get_style_by_name
from prompt_toolkit.styles.pygments import style_from_pygments_cls
from prompt_toolkit import PromptSession
import re
import os

all_themes = [
    "abap","algol","algol_nu","arduino","autumn","bw","borland","coffee","colorful",
    "default","dracula","emacs","friendly_grayscale","friendly","fruity","github-dark",
    "gruvbox-dark","gruvbox-light","igor","inkpot","lightbulb","lilypond","lovelace",
    "manni","material","monokai","murphy","native","nord-darker","nord","one-dark",
    "paraiso-dark","paraiso-light","pastie","perldoc","rainbow_dash","rrt","sas",
    "solarized-dark","solarized-light","staroffice","stata-dark","stata-light","tango",
    "trac","vim","vs","xcode","zenburn"
]

my_themes = [
    "coffee","dracula","github-dark","gruvbox-dark","lightbulb","material",
    "nord-darker","paraiso-dark","zenburn"
]



theme_index = 0 
status_message = ""
current_file = None
syntax_on = True
opened_files = []
file_index = 0

def get_lexer(path: Path):
    ext = path.suffix.lower()
    if ext == ".py":
        return PygmentsLexer(PythonLexer)
    elif ext == ".js":
        return PygmentsLexer(JavascriptLexer)
    elif ext == ".java":
        return PygmentsLexer(JavaLexer)
    elif ext in {".html", ".htm"}:
        return PygmentsLexer(HtmlLexer)
    elif ext == ".sh":
        return PygmentsLexer(BashLexer)
    else:
        return None

def get_style_for_file(path: Path):
    ext = path.suffix.lower()
    if ext == ".py":
        return style_from_pygments_cls(get_style_by_name("material"))
    elif ext == ".sh":
        return style_from_pygments_cls(get_style_by_name("coffee"))
    else:
        return style_from_pygments_cls(get_style_by_name("zenburn"))

def main():
    global current_file, status_message, syntax_on, opened_files, file_index, editor, root_container, app

    file_name = input("\n\n\033[1;33mFile: \033[0m").strip()
    if not file_name:
        file_name = "file.txt"
    current_file = Path(file_name)
    opened_files.append(current_file)
    file_index = 0

    if current_file.exists():
        try:
            text = current_file.read_text(encoding="utf-8")
        except:
            text = ""
    else:
        try:
            current_file.touch()
        except:
            pass
        text = ""

    editor = TextArea(
        text=text,
        lexer=get_lexer(current_file),
        scrollbar=False,
        line_numbers=True,
        wrap_lines=True,
        focus_on_click=True
    )

    output_area = TextArea(
        text="",
        height=4,
        wrap_lines=True,
        focus_on_click=True,
        read_only=False,
        style="bg:black fg:beige bold"
    )

    kb = KeyBindings()
    root_container = FloatContainer(content=HSplit([]), floats=[])

    def clear_status():
        global status_message
        status_message = ""
        app.invalidate()

    @kb.add("c-space")
    def _(event):
        event.app.current_buffer.insert_text("    ")


    @kb.add("c-k")
    def _(event):
        global file_index, current_file, opened_files, editor
        if not opened_files:
            return

        def close_file():
            global file_index
            closed_file = opened_files.pop(file_index)
            if opened_files:
                file_index = file_index % len(opened_files)
                current_file = opened_files[file_index]
                if current_file.exists():
                    try:
                        editor.text = current_file.read_text(encoding="utf-8")
                    except:
                        editor.text = ""
                editor.lexer = get_lexer(current_file) if syntax_on else None
                app.style = get_style_for_file(current_file)
            else:
                # No files left: exit the program
                event.app.exit()
                return

            if confirm_float in root_container.floats:
                root_container.floats.remove(confirm_float)
            app.layout.focus(editor)

        def cancel_close():
            if confirm_float in root_container.floats:
                root_container.floats.remove(confirm_float)
            app.layout.focus(editor)

        dialog = Dialog(
            title="Close Current File?",
            body=TextArea(text="", height=1, read_only=True),
            buttons=[
                Button(text="Yes", handler=close_file),
                Button(text="No", handler=cancel_close)
            ],
            width=40,
            modal=True
        )

        confirm_float = Float(content=dialog)
        root_container.floats.append(confirm_float)
        app.layout.focus(dialog)




    @kb.add("c-s")
    def _(event):
        global status_message
        try:
            current_file.write_text(editor.text, encoding="utf-8")
            status_message = "File saved!"
            app.invalidate()
            asyncio.get_event_loop().call_later(2, clear_status)
        except:
            status_message = "Error saving file"
            app.invalidate()
            asyncio.get_event_loop().call_later(2, clear_status)

    @kb.add("c-f")
    def _(event):
        input_box = TextArea(height=1)

        def ok_handler():
            global current_file, editor, opened_files, file_index, syntax_on
            name = input_box.text.strip()
            if not name:
                return
            p = Path(name)
            if p.exists():
                try:
                    editor.text = p.read_text(encoding="utf-8")
                except:
                    editor.text = ""
            else:
                try:
                    p.touch()
                except:
                    pass
                editor.text = ""
            current_file = p
            if p not in opened_files:
                opened_files.append(p)
                file_index = len(opened_files) - 1
            else:
                file_index = opened_files.index(p)
            syntax_on = True
            editor.lexer = get_lexer(p)
            app.style = get_style_for_file(p)
            if file_float in root_container.floats:
                root_container.floats.remove(file_float)
            app.layout.focus(editor)

        def cancel_handler():
            if file_float in root_container.floats:
                root_container.floats.remove(file_float)
            app.layout.focus(editor)

        input_box.accept_handler = lambda buff: ok_handler()

        dialog = Dialog(
            title="Open File",
            body=input_box,
            buttons=[
                Button(text="OK", handler=ok_handler),
                Button(text="Cancel", handler=cancel_handler)
            ],
            width=40,
            modal=True
        )

        file_float = Float(content=dialog)
        root_container.floats.append(file_float)
        app.layout.focus(input_box)

    @kb.add("c-q")
    def _(event):
        event.app.exit()
    
    @kb.add("c-z")
    def _(event):
        global file_index, current_file
        if not opened_files:
            return
        file_index = (file_index + 1) % len(opened_files)
        current_file = opened_files[file_index]
        if current_file.exists():
            try:
                editor.text = current_file.read_text(encoding="utf-8")
            except:
                editor.text = ""
        editor.lexer = get_lexer(current_file) if syntax_on else None
        app.style = get_style_for_file(current_file)

    @kb.add("c-r")
    def _(event):
        #global status_message
        blocking_words = ["input", "scanf", "cin", "read", "run", "prompt"]
        if any(word in editor.text for word in blocking_words):
            #status_message = "Unable to execute."
            #app.invalidate()
            #asyncio.get_event_loop().call_later(2, lambda : clear_status())
            output_area.text = ""
            output_area.text = "Unable to execute code that uses.\n input(), scanf(), cin >> , etc."

            return


        ext = current_file.suffix.lower()
        cmd = None

        if ext in {".py", ".js"}:
            with tempfile.NamedTemporaryFile("w+", suffix=ext, delete=False) as tmp:
                tmp.write(editor.text)
                tmp.flush()
                tmp_name = tmp.name
            if ext == ".py":
                cmd = ["python", tmp_name]
            elif ext == ".js":
                cmd = ["node", tmp_name]

        elif ext == ".java":
            match = re.search(r'public\s+class\s+(\w+)', editor.text)
            cls_name = match.group(1) if match else "Main"

            tmp_dir = tempfile.gettempdir()
            tmp_name = os.path.join(tmp_dir, f"{cls_name}.java")
            with open(tmp_name, "w", encoding="utf-8") as f:
                f.write(editor.text)

            compile_proc = subprocess.run(["javac", tmp_name], capture_output=True, text=True)
            if compile_proc.returncode != 0:
                output_area.text = compile_proc.stderr
                return
            cmd = ["java", cls_name]

        else:
            output_area.text = "Cannot run this file type."
            return

        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(tmp_name))
            output_area.text = proc.stdout + proc.stderr
        except Exception as e:
            output_area.text = str(e)


    @kb.add("c-x")
    def _(event):
        global theme_index
        global app, status_message
        theme_index = (theme_index + 1) % len(all_themes)
        theme_name = all_themes[theme_index]
        try:
            app.style = style_from_pygments_cls(get_style_by_name(theme_name))
            status_message = f"'{theme_name}'"
        except Exception:
            status_message = f"Theme {theme_name} not available"
        app.invalidate()
        asyncio.get_event_loop().call_later(2, clear_status)

    @kb.add("c-c")
    def _(event):
        global syntax_on, editor, status_message
        syntax_on = not syntax_on
        editor.lexer = get_lexer(current_file) if syntax_on else None
        status_message = "Syntax highlighting ON" if syntax_on else "Syntax highlighting OFF"
        app.invalidate()
        asyncio.get_event_loop().call_later(2, clear_status)

    def status_bar_text():
        d = editor.buffer.document
        msg = f" {current_file}  Ln {d.cursor_position_row+1}  Col {d.cursor_position_col} "
        if status_message:
            msg += f" | {status_message}"
        return [("class:status", msg)]

    status_bar = Window(height=1, content=FormattedTextControl(status_bar_text))

    root_container.content = HSplit([
        Frame(editor),
        status_bar,
        Frame(output_area, title="Program Output")
    ])

    app = Application(
        layout=Layout(root_container, focused_element=editor),
        key_bindings=kb,
        full_screen=True,
        mouse_support=True,
        style=get_style_for_file(current_file)
    )

    app.run()

if __name__ == "__main__":
    main()


