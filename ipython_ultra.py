import readline
import os
import codeop
import tempfile
import keyword
from time import sleep

# ------                                  

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

from pygments.lexers.python import PythonLexer
from pygments.styles import get_style_by_name

# -------
from prompt_toolkit import PromptSession
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.python import PythonLexer
from pygments.styles import get_style_by_name
from prompt_toolkit.styles.pygments import style_from_pygments_cls

excluded = (
    ".mp3",
    ".mp4",
    ".png",
    ".jpg",
    "~",
    ".m4a",
)

files = sorted(
    name
    for name in os.listdir(".")
    if os.path.isfile(name)
    and not name.lower().endswith(excluded)
    and not name.startswith(".")
)


my_style = style_from_pygments_cls(get_style_by_name("material"))

completion_style = Style.from_dict(
    {
        "": "#cccccc",
        "prompt": "bold #ff8800",
        "completion-menu.completion": "bg:#000055 #ffffff",
        "completion-menu.completion.current": "bg:#00ffff #000000",
        "scrollbar.background": "bg:#88aaaa",
        "scrollbar.button": "bg:#222222",
    }
)

style = merge_styles([my_style, completion_style])


custum_words = [
    ".load",
    ".save",
    "%clear",
    "%end",
    "%view",
    "%cat",
    "%edit",
    "%nano",
    "%run",
]

python_words = keyword.kwlist

python_functions = [
    "abs(",
    "acos(",
    "append(",
    "asin(",
    "assert(",
    "atan(",
    "atan2(",
    "bool(",
    "capitalize(",
    "casefold(",
    "ceil(",
    "center(",
    "chr(",
    "clear(",
    "close(",
    "contains(",
    "copy(",
    "cos(",
    "count(",
    "decode(",
    "dict(",
    "divmod(",
    "encode(",
    "endswith(",
    "enumerate(",
    "eval(",
    "exec(",
    "expandtabs(",
    "extend(",
    "filter(",
    "find(",
    "float(",
    "floor(",
    "format(",
    "format_map(",
    "get(",
    "getattr(",
    "hasattr(",
    "hash(",
    "hex(",
    "id(",
    "index(",
    "input(",
    "insert(",
    "int(",
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
    "len(",
    "list(",
    "ljust(",
    "lower(",
    "lstrip(",
    "map(",
    "max(",
    "min(",
    "maketrans(",
    "next(",
    "open(",
    "ord(",
    "partition(",
    "pop(",
    "print(",
    "printf(",
    "Println(",
    "println!(",
    "prompt_toolkit(",
    "range(",
    "read(",
    "reduce(",
    "removeprefix(",
    "removesuffix(",
    "replace(",
    "repr(",
    "reversed(",
    "round(",
    "rfind(",
    "rindex(",
    "rjust(",
    "rpartition(",
    "rsplit(",
    "rstrip(",
    "scanf(",
    "set(",
    "setattr(",
    "sleep(",
    "slice(",
    "sort(",
    "sorted(",
    "split(",
    "splitlines(",
    "startswith(",
    "str(",
    "strip(",
    "sum(",
    "swapcase(",
    "title(",
    "translate(",
    "tuple(",
    "type(",
    "upper(",
    "zfill(",
]

python_libraries = [
    "math",
    "time",
    "random",
    "sys",
    "readline",
    "prompt_toolkit",
    "numpy",
    "scipy",
]

mixed_words = files + custum_words + python_words + python_functions + python_libraries


def get_completer():
    current_files = os.listdir(".")

    return WordCompleter(mixed_words, ignore_case=True)


session = PromptSession(
    lexer=PygmentsLexer(PythonLexer), style=style, auto_suggest=AutoSuggestFromHistory()
)


compiler = codeop.compile_command
buffer = []
local_env = {}
empty_commands = 0

WHITE = "\033[1;38;2;255;255;255m"
YELLOW = "\033[1;38;2;255;255;0m"
ORANGE = "\033[1;38;2;255;165;0m"
CYAN = "\033[1;38;2;0;255;255m"
GREY = "\033[1;38;2;190;190;190m"
RESET = "\033[0m"

os.system("clear")

print(f"\n\n{ORANGE}======[{CYAN} Ipython {YELLOW}Plus {ORANGE}]======{RESET}\n\n\n")
sleep(1)

while True:
    try:
        prompt_text = ">>> " if not buffer else "... "
        line = session.prompt(prompt_text, completer=get_completer())

        if line.strip() == "bash":
            os.system("bash")
            continue

        if line.strip() == "q":
            break

        if line.startswith("%view") or line.startswith("%cat"):
            parts = line.split(maxsplit=1)
            if len(parts) == 2:
                filename = parts[1]

                os.system(f"cat {filename}")
                continue

        # ----- %edit support -----
        if line.startswith("%edit") or line.startswith("%nano"):
            parts = line.split(maxsplit=1)
            if len(parts) == 2:
                filename = parts[1]

                os.system(f"nano {filename}")
            else:
                print("Usage: %edit <filename>")
            continue

        # ----- %run support -----
        if line.startswith("%run"):
            parts = line.split(maxsplit=1)
            if len(parts) == 2:
                filename = parts[1]
                if not os.path.exists(filename):
                    print(f"File '{filename}' not found")
                    continue

                ext = filename.split(".")[-1].lower()
                if ext == "s":
                    obj_file = filename.removesuffix(".s") + "o"
                    exe_file = filename.removesuffix(".s")
                    os.system(
                        f"as {filename} -o {obj_file} && ld -pie {obj_file} -o {exe_file} && ./{exe_file}"
                    )

                elif ext == "py":
                    os.system(f"python3 {filename}")
                if ext == "sh":
                    os.system(f"chmod +x {filename} && bash {filename}")
                elif ext == "c":
                    exe_file = filename.replace(".c", "")

                    compile_cmd = f"gcc {filename} -o {exe_file}"
                    run_cmd = f"./{exe_file}"
                    if os.system(compile_cmd) == 0:
                        os.system(run_cmd)
                elif ext == "go":
                    os.system(f"go run {filename}")
                else:
                    pass
                    # print("Unsupported file type")
            else:
                print("Usage: %run <filename>")
            continue

        # Add line to buffer for multi-line input
        buffer.append(line)
        source = "\n".join(buffer)

        # Track empty lines only inside a block (buffer is not empty)
        if buffer and not line.strip():
            empty_commands += 1
        else:
            empty_commands = 0

        # Try to compile
        code_obj = compiler(source, "<input>", "single")
        if code_obj is None:
            if empty_commands >= 3:
                print(f"\n\n{CYAN}Multiple Empty lines detected.")
                sleep(1)
                print(f"\n\n{YELLOW}Function Canceled.\n\n")
                sleep(1)
                buffer = []
                empty_commands = 0
            continue

        # Execute compiled code
        exec(code_obj, local_env)
        buffer = []
        empty_commands = 0

    except KeyboardInterrupt:
        print("\nKeyboardInterrupt")
        buffer = []
        empty_commands = 0
    except EOFError:
        print("\nExiting")
        break
    except Exception as e:
        sleep(0.6)
        print(f"\n\n{GREY}{type(e).__name__}: {e}\n\n")
        sleep(0.6)
        buffer = []

