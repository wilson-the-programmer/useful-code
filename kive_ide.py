import os
import io
import tempfile
import threading
import traceback
import contextlib
import subprocess
import random

from kivy.config import Config
Config.set("kivy", "window_softinput_mode", "pan")

from kivy.app import App
from kivy.uix.codeinput import CodeInput
from kivy.extras.highlight import PythonLexer
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock

from pygments.styles import STYLE_MAP


editor_top = None
editor_bottom = None
current_editor = None



pygments_styles = ['abap', 'algol', 'algol_nu', 'arduino', 'autumn', 'bw', 'borland', 'coffee', 'colorful', 'default', 'dracula', 'emacs', 'friendly_grayscale', 'friendly', 'fruity', 'github-dark', 'gruvbox-dark', 'gruvbox-light', 'igor', 'inkpot', 'lightbulb', 'lilypond', 'lovelace', 'manni', 'material', 'monokai', 'murphy', 'native', 'nord-darker', 'nord', 'one-dark', 'paraiso-dark', 'paraiso-light', 'pastie', 'perldoc', 'rainbow_dash', 'rrt', 'sas', 'solarized-dark', 'solarized-light', 'staroffice', 'stata-dark', 'stata-light', 'tango', 'trac', 'vim', 'vs', 'xcode', 'zenburn']

pygment_style = random.choice(pygments_styles)


def random_style():

    global editor_top

    text = editor_top.text

    pygment_style = random.choice(pygments_styles)

    editor_top.style_name = pygment_style

    editor_top.text = f"# Style: {pygment_style}\n\n{text}"



def set_console(text, error=False):
    global editor_bottom
    global editor_top

    if error:
        editor_bottom.foreground_color = (1, 0, 0, 1)
    else:
        editor_bottom.foreground_color = (1, 1, 1, 1)

    editor_bottom.text = text
    editor_top.focus = True



def run_python(source):
    output = io.StringIO()

    try:
        with contextlib.redirect_stdout(output):
            exec(source, {"__name__": "__main__"})

        return output.getvalue()

    except Exception:
        return traceback.format_exc()


def run_compiled(source, language):

    ext = "c" if language == "C" else "cpp"
    compiler = "gcc" if language == "C" else "g++"

    try:
        with tempfile.TemporaryDirectory() as folder:

            source_file = os.path.join(folder, "program." + ext)
            executable = os.path.join(folder, "program")

            with open(source_file, "w", encoding="utf-8") as f:
                f.write(source)

            compile_result = subprocess.run(
                [compiler, source_file, "-o", executable],
                capture_output=True,
                text=True
            )

            if compile_result.returncode != 0:
                return compile_result.stderr

            os.chmod(executable, 0o755)

            result = subprocess.run(
                [executable],
                capture_output=True,
                text=True
            )

            return result.stdout + result.stderr

    except Exception:
        return traceback.format_exc()


def run_bash(source):

    try:
        result = subprocess.run(
            ["sh", "-c", source],
            capture_output=True,
            text=True
        )

        return result.stdout + result.stderr

    except Exception:
        return traceback.format_exc()


def execute_code(language):

    global current_editor

    source = current_editor.text
    editor_bottom.text = ""

    def worker():

        if language == "Python":
            result = run_python(source)

        elif language == "Bash":
            result = run_bash(source)

        else:
            result = run_compiled(source, language)

        Clock.schedule_once(
            lambda dt: set_console(result, "Traceback" in result)
        )

    threading.Thread(
        target=worker,
        daemon=True
    ).start()

def set_active(widget, focus):

    global current_editor

    if focus:
        current_editor = widget



def create_ui():

    global editor_top
    global editor_bottom
    global current_editor


    root = BoxLayout(
        orientation="vertical"
    )


    buttons = BoxLayout(
        size_hint_y=None,
        height=80,
        spacing=5,
        padding=5
    )


    python_button = Button(
        text="Python",
        font_size=36,
        size_hint_x=None,
        width=150
    )

    c_button = Button(
        text="C >",
        font_size=36,
        size_hint_x=None,
        width=130
    )

    cpp_button = Button(
        text="C++",
        font_size=36,
        size_hint_x=None,
        width=130
    )

    bash_button = Button(
        text="Bash",
        font_size=36,
        size_hint_x=None,
        width=130
    )
    
    style_button = Button(
        text="Style",
        font_size=36,
        size_hint_x=None,
        width=130
    )




    buttons.add_widget(python_button)
    buttons.add_widget(c_button)
    buttons.add_widget(cpp_button)
    buttons.add_widget(bash_button)
    buttons.add_widget(style_button)


    editor_top = CodeInput(
        lexer=PythonLexer(),
        style_name="lightbulb",
        font_size=32,
        padding=15,
        size_hint_y=0.22,
        background_color=(0, 0, 0, 1),
        foreground_color=(0.9, 0.9, 0.9, 1),
        cursor_color = (0, 1, 1, 1)
    )
    



    editor_bottom = CodeInput(
        lexer=PythonLexer(),
        font_size=32,
        padding=15,
        size_hint_y=0.35,
        foreground_color=(1, 1, 1, 1),
        background_color=(0, 0, 0, 1),
        style_name="xcode",
        #readonly=True
    )


    current_editor = editor_top


    editor_top.bind(
        focus=set_active
    )


    python_button.bind(
        on_release=lambda x: execute_code("Python")
    )

    c_button.bind(
        on_release=lambda x: execute_code("C")
    )

    cpp_button.bind(
        on_release=lambda x: execute_code("C++")
    )

    bash_button.bind(
        on_release=lambda x: execute_code("Bash")
    )

    style_button.bind(
        on_release=lambda x: random_style()
    )
    
    
    


    root.add_widget(buttons)
    root.add_widget(editor_top)
    root.add_widget(editor_bottom)


    return root



class MainApp(App):

    def build(self):

        return create_ui()



MainApp().run()
