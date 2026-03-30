import os
import readline
import atexit
import subprocess
import random


# Bold truecolor ANSI codes
WHITE = "\001\033[1;38;2;255;255;255m\002"
YELLOW = "\001\033[1;38;2;255;255;0m\002"
ORANGE = "\001\033[1;38;2;255;165;0m\002"
LIGHT_BLUE = "\001\033[1;38;2;173;216;230m\002"
CYAN = "\001\033[1;38;2;0;255;255m\002"
BEIGE = "\001\033[1;38;2;245;245;220m\002"

RESET = "\001\033[0m\002"



# List of all color variables
colors = [
    WHITE,
    YELLOW,
    ORANGE,
    LIGHT_BLUE,
    CYAN,
    BEIGE
]



# Persistent history
histfile = os.path.expanduser("~/.shell_history")
try:
    readline.read_history_file(histfile)
except FileNotFoundError:
    pass

readline.set_history_length(1000)
atexit.register(readline.write_history_file, histfile)

# Tab completion
import rlcompleter
readline.parse_and_bind("tab: complete")

while True:
    prompt_color = random.choice(colors)
    current_dir = os.getcwd()
    try:
        command = input(f"\n{CYAN}{current_dir} {prompt_color}$ {WHITE}").strip()

        if not command:
            continue
        if command in ("exit", "q"):
            break
        if command in ("cd", "home"):
            os.chdir(os.path.expanduser("~"))

        # Built-in cd
        if command.startswith("cd "):
            path = command[3:].strip()
            try:
                os.chdir(os.path.expanduser(path))
            except FileNotFoundError:
                print(f"No such directory: {path}")
            continue

        # Run other commands
        subprocess.run(command, shell=True)

    except KeyboardInterrupt:
        print()  # handle Ctrl+C gracefully
    except EOFError:
        break