import os
import re
import time
from collections import defaultdict
from halo import Halo

try:
    file = input("\nFile: ").strip()
    lint_output = f"{file}_lint_msg.txt"

    time.sleep(1)
    os.system('printf "\\n\\nSeveral processes occurring.\\n\\nPlease be patient.\\n\\nNote: The longer the file the longer this is going to take. This could take anywhere from 10 seconds to 2 minutes.\\n\\n⏰🕛\\n\\n"')
    time.sleep(1)

    spinner = Halo(text=' ', spinner='dots')
    spinner.start()

    os.system(f"black {file}")
    os.system(f"printf '\n\n'")
    os.system(f"pylint {file} > {lint_output}")

    spinner.stop()

    with open(lint_output, "r") as f:
        lines = f.readlines()

    filename = None
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
                filename = match.group(1)
                line_number = int(match.group(2))
                message = match.group(3).strip()
                symbol = match.group(4).strip()
                issues[line_number].append(f"• {message} ({symbol})")

    sorted_lines = sorted(issues.keys())

    output = []

    if filename:
        output.append(f"File '{filename}'\n")

    for num in sorted_lines:
        output.append(f"\nLine {num}:\n")
        for msg in issues[num]:
            output.append(f"\n{msg}\n")

    if code_score is not None:
        output.append(f"\nCode Score: {code_score:.2f} / 10\n")

    with open(lint_output, "w") as f:
        f.write("\n".join(output))

    os.system(f'printf "\\n\\nAll Done! ✨ 🍰\\n\\n    \'{lint_output}\' ready to read.\\n\\n"')

    time.sleep(1.5)
    read_file = input(f"\n\nDo you want to read '{lint_output}'?\n\n    1) Yes\n    2) No\n\n").strip().lower()

    if read_file in ['1', 'yes', 'y']:
        os.system(f"cat {lint_output}")
    else:
        os.system('printf "\\n\\nOkay...Well have a good day!\\n\\n"')
        time.sleep(1)

except Exception as e:
    print(f"\n\n{e}\n\n")

