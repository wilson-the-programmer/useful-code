import readline
import os
import subprocess
import tempfile
from time import sleep

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
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
    'JSON',
    'Map',
    'Math',
    'Number',
    'Object',
    'Promise',
    'RegExp',
    'Set',
    'String',
    'Symbol',
    'WeakMap',
    'WeakSet',
    'console',
    'document',
    'globalThis',
    'Infinity',
    'NaN',
    'undefined',
    'null',
    'true',
    'false',
    'let',
    'const',
    'var',
    'function',
    'return',
    'if',
    'else',
    'for',
    'while',
    'do',
    'switch',
    'case',
    'break',
    'continue',
    'try',
    'catch',
    'finally',
    'throw',
    'class',
    'extends',
    'new',
    'this',
    'super',
    'import',
    'export',
    'default',
    'async',
    'await',
    'typeof',
    'instanceof',
    'in',
    'of',
    'delete',
    'void',
    'yield',
    'debugger',
    'eval',
    'parseInt',
    'parseFloat',
    'isNaN',
    'isFinite',
    'setTimeout',
    'setInterval',
    'clearTimeout',
    'clearInterval'
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
empty_commands = 0

WHITE = "\033[1;38;2;255;255;255m"
YELLOW = "\033[1;38;2;255;255;0m"
ORANGE = "\033[1;38;2;255;165;0m"
CYAN = "\033[1;38;2;0;255;255m"
GREY = "\033[1;38;2;190;190;190m"
RESET = "\033[0m"


def execute_javascript():
    global buffer
    global empty_commands

    if not buffer:
        print(f"{YELLOW}Buffer is empty.{RESET}")
        return

    source = "\n".join(buffer)
    filename = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".js",
            delete=False
        ) as temp_file:
            temp_file.write(source)
            filename = temp_file.name

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

        if line.strip() == "q":
            break

        if line.strip() == "%clear":
            buffer = []
            empty_commands = 0
            print(f"{CYAN}Buffer cleared.{RESET}")
            continue

        if line.strip() == "%end":
            execute_javascript()
            continue

        if line.startswith("%view") or line.startswith("%cat"):
            parts = line.split(maxsplit=1)

            if len(parts) == 2:
                filename = parts[1]
                os.system(f"cat {filename}")
            else:
                print("Usage: %view <filename>")

            continue

        if line.startswith("%edit") or line.startswith("%nano"):
            parts = line.split(maxsplit=1)

            if len(parts) == 2:
                filename = parts[1]
                os.system(f"nano {filename}")
            else:
                print("Usage: %edit <filename>")

            continue

        if line.startswith("%run"):
            parts = line.split(maxsplit=1)

            if len(parts) == 2:
                filename = parts[1]

                if not os.path.exists(filename):
                    print(f"File '{filename}' not found")
                    continue

                extension = filename.split(".")[-1].lower()

                if extension == "js":
                    subprocess.run(["node", filename])
                else:
                    print("Unsupported file type")
            else:
                print("Usage: %run <filename>")

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

