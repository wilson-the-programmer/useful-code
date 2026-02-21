import os
import re
import time
from collections import defaultdict
from halo import Halo
import sys

RESET = "\033[0m"
WHITE = "\033[1;38;2;255;255;255m"
YELLOW = "\033[1;38;2;255;255;0m"
ORANGE = "\033[1;38;2;255;165;0m"
CYAN = "\033[1;38;2;0;255;255m"
GREEN = "\033[1;38;2;0;255;0m"
RED = "\033[1;38;2;255;0;0m"
MAGENTA = "\033[1;38;2;255;0;255m"
BLUE = "\033[1;38;2;0;0;255m"
BEIGE = "\033[1;38;2;245;245;220m"
LIGHT_PINK = "\033[1;38;2;255;182;193m"
LIGHT_ORANGE = "\033[1;38;2;255;200;100m"
LIME = "\033[1;38;2;191;255;0m"
TURQUOISE = "\033[1;38;2;64;224;208m"

def ghost_type(text, delay=0.03, color_code=f"{CYAN}"):
    reset_code = "\033[0m"
    for char in text:
        sys.stdout.write(f"{color_code}{char}{reset_code}")
        sys.stdout.flush()
        time.sleep(delay)
    print()

try:
    file = input(f"\n{ORANGE}File: {CYAN}").strip()

    if not os.path.isfile(file):
        ghost_type(f"\n\n{RED}The file{YELLOW} '{file}'{RED} does not exist.\n\n")
        time.sleep(1)
        ghost_type(f"{YELLOW}Okay...Well have a good day!\n\n")
        time.sleep(1)
        sys.exit()

    lint_output = "lint_analysis.txt"

    time.sleep(1)
    ghost_type(
        "\n\nSeveral processes occurring.\n\n"
        "Please be patient.\n\n"
        "Note: The longer the file the longer this is going to take.\n\n⏰🕛\n\n"
    )
    time.sleep(1)

    spinner = Halo(text="  ", spinner="dots")
    spinner.start()

    os.system(f"pylint {file} > {lint_output}")

    spinner.stop()

    with open(lint_output, "r") as f:
        lines = f.readlines()

    issues = defaultdict(list)
    code_score = None

    for line in lines:
        if line.startswith("************* Module"):
            continue
        score_match = re.search(r"Your code has been rated at ([\d\.]+)/10", line)
        if score_match:
            code_score = float(score_match.group(1))
            continue
        if ":" in line and "(" in line:
            match = re.match(r"(.+?):(\d+):\d+:\s+[A-Z]\d+:\s+(.*?)\s+\((.*?)\)", line)
            if match:
                line_number = int(match.group(2))
                message = match.group(3).strip()
                symbol = match.group(4).strip()
                issues[line_number].append(f"• {message} ({symbol})")

    sorted_lines = sorted(issues.keys())

    output = []
    output.append(f"File: '{file}'\n")

    for num in sorted_lines:
        output.append(f"\nLine {num}:\n")
        for msg in issues[num]:
            output.append(f"\n{msg}\n")

    if code_score is not None:
        output.append(f"\nCode Score: {code_score:.2f} / 10\n")

    with open(lint_output, "w") as f:
        f.write("\n".join(output))

    ghost_type(f"\n\nAll Done! ✨ 🍰\n\n    '{lint_output}' ready to read.\n\n")

    time.sleep(1.5)
    read_file = (
        input(
            f"\n\n{ORANGE}Do you want to read {CYAN}'{lint_output}'?{WHITE}\n\n    1) Yes\n    2) No\n\n"
        )
        .strip()
        .lower()
    )

    if read_file in ["1", "yes", "y"]:
        os.system(f"printf '\n\n{BEIGE}'")
        os.system(f"cat {lint_output}")
    else:
        ghost_type("\n\nOkay...Well have a good day!\n\n")
        time.sleep(1)

except Exception as e:
    ghost_type(f"\n\n{e}\n\n")
