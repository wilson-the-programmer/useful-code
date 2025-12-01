
import tempfile
import subprocess
import os
from time import sleep
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers import JavascriptLexer
from prompt_toolkit.styles.pygments import style_from_pygments_cls
from pygments.styles import get_style_by_name
from prompt_toolkit import PromptSession


temp = tempfile.NamedTemporaryFile(mode="a+", delete=False, suffix=".js")
filename = temp.name
temp.close()

style = style_from_pygments_cls(get_style_by_name("lightbulb"))

session = PromptSession(
    lexer=PygmentsLexer(JavascriptLexer),
    style=style
)

js_keywords = [
    "var","let","const","function","return","if","else","for","while",
    "do","switch","case","break","continue","try","catch","finally",
    "throw","import","export","class","new","this","super","extends",
    "constructor","console.log", "{", "}", "(", ")", "[", "]"
]

def is_math_expression(s):
    try:
        eval(s, {"__builtins__": None}, {"Math": __import__("math")})
        return True
    except:
        return False

def eval_math_expression(s):
    return eval(s, {"__builtins__": None}, {"Math": __import__("math")})

while True:
    try:
        command = session.prompt("\nJS> ").strip()
        cmd = command.lower()

        if cmd in ["exit", "quit"]:
            break

        if cmd.startswith("rm ln"):
            try:
                n = cmd.split()[2]
                subprocess.run(["sed", "-i", f"{n}d", filename])
            except:
                pass
            continue

        if is_math_expression(command):
            print(f"\n\033[1;33m{eval_math_expression(command)}\033[0m")
            continue

        if any(k in cmd for k in js_keywords) and cmd not in ["run","program","%run"]:
            with open(filename, "a") as f:
                f.write(command + "\n")

        if "run" in cmd or "program" in cmd or "%run" in cmd:
            subprocess.run(["node", filename])
        elif "edit" in cmd:
            subprocess.run(["vim", filename])
        elif "see" in cmd or "code" in cmd:
            subprocess.run(["cat", filename])

    except KeyboardInterrupt:
        continue
    except EOFError:
        break
