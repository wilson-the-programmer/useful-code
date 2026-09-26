
import readline
import os
import subprocess
import tempfile
from time import sleep

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.widgets import TextArea
from prompt_toolkit.application import Application
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style, merge_styles
from prompt_toolkit.styles.pygments import style_from_pygments_cls

from pygments.lexers.javascript import JavascriptLexer
from pygments.styles import get_style_by_name


javascript_words = [
    'Array',
    'Boolean',
    'Date',
    'Error',
    'Function',
    'Infinity',
    'JSON',
    'Map',
    'Math',
    'NaN',
    'Number',
    'Object',
    'Promise',
    'RegExp',
    'Set',
    'String',
    'Symbol',
    'WeakMap',
    'WeakSet',
    'async',
    'await',
    'break',
    'case',
    'catch',
    'class',
    'clearInterval(',
    'clearTimeout(',
    'console',
    'const',
    'continue',
    'debugger',
    'default',
    'delete',
    'do',
    'document',
    'else',
    'eval(',
    'export',
    'extends',
    'false',
    'finally',
    'for',
    'function',
    'globalThis',
    'if',
    'import',
    'in',
    'instanceof',
    'isFinite(',
    'isNaN(',
    'let',
    'log(',
    'new',
    'null',
    'of',
    'parseFloat(',
    'parseInt(',
    'return',
    'setInterval(',
    'setTimeout(',
    'super',
    'switch',
    'this',
    'throw',
    'true',
    'try',
    'typeof',
    'undefined',
    'var',
    'void',
    'while',
    'with',
    'yield',
    ".help",
    ".exit",
    ".editor",
    ".edit",
    ".load",
    ".save",
    "%clear",
    "%end",
    "%view",
    "%cat",
    "%edit",
    "%nano",
    "%run"

]


one_dark_style = style_from_pygments_cls(
    get_style_by_name("one-dark")
)

completion_style = Style.from_dict({
    '': '#cccccc',
    'prompt': 'bold #ff8800',
    'completion-menu.completion': 'bg:#008888 #ffffff',
    'completion-menu.completion.current': 'bg:#00aaaa #000000',
    'scrollbar.background': 'bg:#88aaaa',
    'scrollbar.button': 'bg:#222222',
})

style = merge_styles([
    one_dark_style,
    completion_style
])


def get_completer():
    current_files = os.listdir('.')

    return WordCompleter(
        javascript_words + current_files,
        ignore_case=True
    )


session = PromptSession(
    lexer=PygmentsLexer(JavascriptLexer),
    style=style,
    auto_suggest=AutoSuggestFromHistory()
)


buffer = []
evaluated_commands = []
empty_commands = 0

WHITE = "\033[1;38;2;255;255;255m"
YELLOW = "\033[1;38;2;255;255;0m"
ORANGE = "\033[1;38;2;255;165;0m"
CYAN = "\033[1;38;2;0;255;255m"
GREY = "\033[1;38;2;190;190;190m"
RESET = "\033[0m"


def execute_source(source):
    global buffer
    global empty_commands

    if not source.strip():
        print(f"{YELLOW}Buffer is empty.{RESET}")
        return

    filename = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".js",
            delete=False
        ) as temp_file:
            temp_file.write(source)
            filename = temp_file.name

        evaluated_commands.append(source)

        result = subprocess.run(
            ["node", filename],
            text=True,
            capture_output=True
        )

        if result.stdout:
            print(result.stdout, end="")

        if result.stderr:
            print(f"{GREY}{result.stderr}{RESET}", end="")

    except FileNotFoundError:
        print(f"{YELLOW}Node.js was not found.{RESET}")

    finally:
        if filename and os.path.exists(filename):
            os.remove(filename)

    buffer = []
    empty_commands = 0


def execute_javascript():
    global buffer

    if not buffer:
        print(f"{YELLOW}Buffer is empty.{RESET}")
        return

    source = "\n".join(buffer)
    execute_source(source)


def load_javascript(filename):
    filename = filename.strip()

    if not os.path.exists(filename):
        print(f"{YELLOW}File '{filename}' not found.{RESET}")
        return

    try:
        with open(filename, "r") as javascript_file:
            source = javascript_file.read()

        execute_source(source)

    except OSError as error:
        print(f"{YELLOW}{error}{RESET}")


def save_session(filename):
    filename = filename.strip()

    if not evaluated_commands:
        print(f"{YELLOW}No evaluated commands to save.{RESET}")
        return

    try:
        with open(filename, "w") as javascript_file:
            javascript_file.write(
                "\n\n".join(evaluated_commands)
            )

        print(f"{CYAN}Session saved to {filename}{RESET}")

    except OSError as error:
        print(f"{YELLOW}{error}{RESET}")


def print_help():
    print(
        f"""
{CYAN}.help{RESET}             Show this help
{CYAN}.exit{RESET}             Exit Javascript Plus
{CYAN}.editor{RESET}          Enter multiline editor
{CYAN}.edit{RESET}            Enter multiline editor
{CYAN}.load <file>{RESET}     Load and execute a JavaScript file
{CYAN}.save <file>{RESET}     Save evaluated commands
{CYAN}%clear{RESET}            Clear the current buffer
{CYAN}%end{RESET}              Execute the current buffer
{CYAN}%view <file>{RESET}     Display a file
{CYAN}%cat <file>{RESET}      Display a file
{CYAN}%edit <file>{RESET}     Edit a file with nano
{CYAN}%nano <file>{RESET}     Edit a file with nano
{CYAN}%run <file>{RESET}      Run a JavaScript file
{CYAN}q{RESET}                Exit Javascript Plus
"""
    )


def run_editor():
    editor = TextArea(
        text="",
        lexer=PygmentsLexer(JavascriptLexer),
        completer=get_completer(),
        scrollbar=True,
        line_numbers=True,
        multiline=True,
        wrap_lines=False,
        focus_on_click=True
    )

    key_bindings = KeyBindings()

    @key_bindings.add("c-d")
    def handle_ctrl_d(event):
        event.app.exit(result=editor.text)

    @key_bindings.add("c-c")
    def handle_ctrl_c(event):
        event.app.exit(result=None)

    application = Application(
        layout=Layout(editor),
        key_bindings=key_bindings,
        style=style,
        full_screen=True,
        mouse_support=False
    )

    try:
        source = application.run()

        if source is None:
            print(f"\n{YELLOW}Editor input aborted.{RESET}")
            return

        lines = source.splitlines()

        while lines and not lines[-1].strip():
            lines.pop()

        if lines and lines[-1].strip() == "%end":
            lines.pop()

        source = "\n".join(lines)

        if source.strip():
            execute_source(source)
        else:
            print(f"{YELLOW}Editor buffer is empty.{RESET}")

    except KeyboardInterrupt:
        print(f"\n{YELLOW}Editor input aborted.{RESET}")


os.system("clear")

print(
    f"\n\n{ORANGE}======[{CYAN} Javascript "
    f"{YELLOW}Plus {ORANGE}]======{RESET}\n\n\n"
)

sleep(1)

while True:
    try:
        prompt_text = ">>> " if not buffer else "... "

        line = session.prompt(
            prompt_text,
            completer=get_completer()
        )

        command = line.strip()

        if command == "q":
            break

        if command == ".exit":
            break

        if command == ".help":
            print_help()
            continue

        if command == ".editor" or command == ".edit":
            run_editor()
            continue

        if command.startswith(".load"):
            parts = line.split(maxsplit=1)

            if len(parts) == 2:
                load_javascript(parts[1].strip())
            else:
                print(f"{YELLOW}Usage: .load <filename>{RESET}")

            continue

        if command.startswith(".save"):
            parts = line.split(maxsplit=1)

            if len(parts) == 2:
                save_session(parts[1].strip())
            else:
                print(f"{YELLOW}Usage: .save <filename>{RESET}")

            continue

        if command == "%clear":
            buffer = []
            empty_commands = 0
            print(f"{CYAN}Buffer cleared.{RESET}")
            continue

        if command == "%end":
            execute_javascript()
            continue

        if line.startswith("%view") or line.startswith("%cat"):
            parts = line.split(maxsplit=1)

            if len(parts) == 2:
                filename = parts[1].strip()
                os.system(f"cat {filename}")
            else:
                print(f"{YELLOW}Usage: %view <filename>{RESET}")

            continue

        if line.startswith("%edit") or line.startswith("%nano"):
            parts = line.split(maxsplit=1)

            if len(parts) == 2:
                filename = parts[1].strip()
                os.system(f"nano {filename}")
            else:
                print(f"{YELLOW}Usage: %edit <filename>{RESET}")

            continue

        if line.startswith("%run"):
            parts = line.split(maxsplit=1)

            if len(parts) == 2:
                filename = parts[1].strip()

                if not os.path.exists(filename):
                    print(f"{YELLOW}File '{filename}' not found{RESET}")
                    continue

                extension = filename.split(".")[-1].lower()

                if extension == "js":
                    subprocess.run(["node", filename])
                else:
                    print(f"{YELLOW}Unsupported file type{RESET}")
            else:
                print(f"{YELLOW}Usage: %run <filename>{RESET}")

            continue

        buffer.append(line)

        if line.strip():
            empty_commands = 0
        else:
            empty_commands += 1

        if empty_commands >= 3:
            execute_javascript()

    except KeyboardInterrupt:
        print("\nKeyboardInterrupt")
        buffer = []
        empty_commands = 0

    except EOFError:
        print("\nExiting")
        break

    except Exception as error:
        sleep(0.6)
        print(
            f"\n\n{GREY}{type(error).__name__}: "
            f"{error}\n\n{RESET}"
        )
        sleep(0.6)
        buffer = []
        empty_commands = 0

print("GoodBye!")


"""
Read


**JavaScript Plus** is a next-generation interactive JavaScript environment that transforms how developers test, experiment, and execute code. It's more than a REPL—it's a complete development companion tailored for modern JavaScript workflows.

**Core Features:**

- **Interactive REPL**: Write and execute JavaScript instantly with live output, just like Node.js but with a beautiful, refined interface
- **Intelligent Auto-Completion**: Smart suggestions for JavaScript keywords, methods, and local files—so you stay in flow without breaking focus
- **Multi-line Editor**: Escape the single-line constraint. Press `.editor` to enter a full-screen, syntax-highlighted editor for complex code blocks
- **Session Management**: Save your work with `.save` and load entire JavaScript files with `.load` for continuity between sessions
- **Syntax Highlighting**: Professional One Dark theme with color-coded JavaScript syntax for clarity and aesthetics
- **Advanced Commands**: Buffer control (`%clear`, `%end`), file operations (`%view`, `%cat`, `%edit`), and direct execution (`%run`)
- **Keyboard Shortcuts**: Ctrl+D to execute, Ctrl+C to cancel—streamlined for efficiency
- **Auto-Execute**: Type three blank lines and your buffer executes automatically—no extra commands needed

**Perfect for:**

- Rapid prototyping and algorithm testing
- Learning JavaScript interactively
- Quick debugging and experimentation
- Running utility scripts on the fly
- Building and iterating on code snippets

JavaScript Plus delivers the speed and responsiveness developers demand—a lightweight yet powerful tool that sits between a basic REPL and a full IDE. It's designed for productivity, elegance, and the modern JavaScript developer's workflow.

"""




