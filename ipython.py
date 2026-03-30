import readline
import os
import codeop
import tempfile
from time import sleep

from prompt_toolkit import PromptSession
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.python import PythonLexer
from pygments.styles import get_style_by_name
from prompt_toolkit.styles.pygments import style_from_pygments_cls

current_theme_name = "material"
current_style = style_from_pygments_cls(get_style_by_name(current_theme_name))
session = PromptSession(lexer=PygmentsLexer(PythonLexer), style=current_style)


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
        line = session.prompt(prompt_text)

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
                if ext == "py":
                    os.system(f"python3 {filename}")
                if ext == "sh":
                    os.system(f"chmod +x {filename} && bash {filename}")
                elif ext == "c":
                    # Use tempfile for C compilation
                    with tempfile.NamedTemporaryFile(delete=False) as tmp:
                        exe_name = tmp.name
                    compile_cmd = f"gcc {filename} -o {exe_name}"
                    run_cmd = f"{exe_name}"
                    if os.system(compile_cmd) == 0:
                        os.system(run_cmd)
                    os.remove(exe_name)
                elif ext == "go":
                    os.system(f"go run {filename}")
                else:
                    print("Unsupported file type")
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
