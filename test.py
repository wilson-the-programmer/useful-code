import tempfile
import subprocess
import os
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers import JavascriptLexer
from prompt_toolkit.styles.pygments import style_from_pygments_cls
from pygments.styles import get_style_by_name
from prompt_toolkit import PromptSession
from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Number, Operator, Text

# Temporary file to store code
temp = tempfile.NamedTemporaryFile(mode="a+", delete=False, suffix=".js")
filename = temp.name
temp.close()

# Pygments lightbulb style
style = style_from_pygments_cls(get_style_by_name("lightbulb"))

# Prompt session
session = PromptSession(
    lexer=PygmentsLexer(JavascriptLexer),
    style=style
)

# JS keywords list (lowercase, plus console.log)
js_keywords = [
    "var","let","const","function","return","if","else","for","while",
    "do","switch","case","break","continue","try","catch","finally",
    "throw","import","export","class","new","this","super","extends",
    "constructor","console.log","{","}","(",")","[","]"
]

# Check if string is a math expression
def is_math_expression(s):
    try:
        eval(s, {"__builtins__": None}, {"Math": __import__("math")})
        return True
    except:
        return False

def eval_math_expression(s):
    return eval(s, {"__builtins__": None}, {"Math": __import__("math")})

# Custom Pygments style for bold yellow keywords
class JSTempStyle(Style):
    default_style = ""
    styles = {
        Keyword: "bold ansiyellow",
        Name: "",
        Comment: "italic",
        String: "ansigreen",
        Number: "ansimagenta",
        Operator: "ansiblue",
        Text: "",
    }

while True:
    try:
        command = session.prompt("\nJS> ").strip()
        cmd = command.lower()

        # Exit commands
        if cmd in ["exit", "quit"]:
            break

        # Remove line command
        if cmd.startswith("rm ln"):
            try:
                n = cmd.split()[2]
                subprocess.run(["sed", "-i", f"{n}d", filename])
            except:
                pass
            continue

        # Evaluate math expressions
        if is_math_expression(command):
            print(f"\n\033[1;33m{eval_math_expression(command)}\033[0m")
            continue

        # Append code lines (ignore run/program/%run)
        if any(k in cmd for k in js_keywords) and cmd not in ["run","program","%run"]:
            with open(filename, "a") as f:
                f.write(command + "\n")

        # Run JS program
        if "run" in cmd or "program" in cmd or "%run" in cmd:
            subprocess.run(["node", filename])
        # Edit file
        elif "edit" in cmd:
            subprocess.run(["vim", filename])
        # Show code with highlighting and line numbers
        elif cmd == "code":
            subprocess.run([
                "pygmentize",
                "-l", "javascript",
                "-f", "terminal",
                "-O", f"style={JSTempStyle.__name__},linenos=1",
                filename
            ])
        # Show code plain
        elif cmd == "see":
            subprocess.run(["cat", filename])

    except KeyboardInterrupt:
        continue
    except EOFError:
        break
