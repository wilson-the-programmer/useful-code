from time import sleep
import re
import shutil

RESET = "\033[0m"
ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
terminal_width = shutil.get_terminal_size().columns

variable_color = "\033[1;38;2;255;140;0m"
string_color = "\033[1;38;2;173;216;230m"
preprocessor_color = "\033[1;38;2;255;215;0m"

all_keywords = list({
    "False","None","True","and","as","assert","async","await","break","class",
    "continue","def","del","elif","else","except","finally","for","from","global",
    "if","import","in","is","lambda","nonlocal","not","or","pass","raise","return",
    "try","while","with","yield","match",
    "auto","case","char","const","default","do","double","enum","extern","float",
    "goto","inline","int","long","register","restrict","short","signed","sizeof",
    "static","struct","switch","typedef","union","unsigned","void","volatile",
    "_Alignas","_Alignof","_Atomic","_Bool","_Complex","_Generic","_Imaginary",
    "_Noreturn","_Static_assert","_Thread_local",
    "crate","false","fn","impl","let","loop","mod","move","mut","pub","ref",
    "self","Self","super","trait","type","unsafe","use","where","dyn","abstract",
    "become","box","final","macro","override","priv","try","typeof","unsized",
    "virtual","yield"
})

def generate_vivid_colors(n):
    base_colors = [
        (255, 255, 0), (255, 165, 0), (0, 255, 255), (255, 215, 0),
        (173, 216, 230), (245, 245, 220), (255, 228, 181), (240, 230, 140),
        (255, 218, 185), (238, 232, 170)
    ]
    colors = []
    for i in range(n):
        r, g, b = base_colors[i % len(base_colors)]
        r = (r + i * 13) % 256
        g = (g + i * 17) % 256
        b = (b + i * 23) % 256
        colors.append(f"\033[1;38;2;{r};{g};{b}m")
    return colors

keyword_colors = {kw: col for kw, col in zip(all_keywords, generate_vivid_colors(len(all_keywords)))}
pattern = re.compile(r'(?<!\w)(' + '|'.join(re.escape(kw) for kw in all_keywords) + r')(?!\w)')

preprocessor_patterns = [
    r'#include\s*<[^>]+>',
    r'#define\b.*'
]
preprocessor_regex = re.compile('|'.join(preprocessor_patterns))

def wrap_ansi(text, width):
    words = re.findall(r'\S+|\n', text)
    lines = []
    current_line = ''
    for word in words:
        if word == '\n':
            lines.append(current_line)
            current_line = ''
            continue
        plain_len = len(ansi_escape.sub('', current_line))
        word_len = len(ansi_escape.sub('', word))
        if plain_len + word_len + (1 if current_line else 0) <= width:
            if current_line:
                current_line += ' '
            current_line += word
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

def highlight_code(text):
    text = re.sub(r'(\".*?\"|\'.*?\')', lambda m: f"{string_color}{m.group(0)}{RESET}", text)
    text = pattern.sub(lambda m: f"{keyword_colors[m.group(0)]}{m.group(0)}{RESET}", text)
    text = re.sub(r'(\b\w+\b)(?=\s*=)', lambda m: f"{variable_color}{m.group(1)}{RESET}", text)
    text = preprocessor_regex.sub(lambda m: f"{preprocessor_color}{m.group(0)}{RESET}", text)
    return text

filename = input("Enter filename: ").strip()

try:
    with open(filename, "r") as f:
        content = f.read()
except FileNotFoundError:
    print(f"File '{filename}' not found.")
    exit(1)

wrapped_lines = wrap_ansi(content, terminal_width)
highlighted_lines = [highlight_code(line) for line in wrapped_lines]

for line in highlighted_lines:
    for char in line:
        print(char, end="", flush=True)
        sleep(0.07)
    print()
    