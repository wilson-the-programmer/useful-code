import sys
import os
import re
import keyword
import tempfile
import subprocess

from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QAction,
    QKeySequence,
    QSyntaxHighlighter,
    QTextCharFormat,
    QColor,
    QFont,
)

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTextEdit,
    QFileDialog,
    QWidget,
    QVBoxLayout,
    QSplitter,
)

from PySide6.QtWidgets import QToolBar, QStyle

cpp_words = ["int", "std", "char", "double", "true", "false", "auto", "case", "void"]

python_functions = [
    "abs",
    "all",
    "any",
    "bin",
    "chr",
    "dict",
    "dir",
    "enumerate",
    "eval",
    "exec",
    "float",
    "format",
    "hasattr",
    "hex",
    "id",
    "input",
    "int",
    "isinstance",
    "len",
    "list",
    "map",
    "max",
    "min",
    "oct",
    "open",
    "ord",
    "print",
    "range",
    "round",
    "set",
    "sorted",
    "str",
    "sum",
    "tuple",
    "type",
    "zfill",
]


class PythonHighlighter(QSyntaxHighlighter):

    def __init__(self, document):
        super().__init__(document)

        self.rules = []

        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#c68eeb"))

        for word in keyword.kwlist + python_functions + cpp_words:
            self.rules.append((re.compile(rf"\b{word}\b"), keyword_format))

        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#9fbba7"))

        self.rules.append((re.compile(r'"[^"]*"|\'[^\']*\''), string_format))

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#888888"))

        self.rules.append((re.compile(r"#[^\n]*"), comment_format))

        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#9eb9eb"))

        self.rules.append((re.compile(r"\b\d+(\.\d+)?\b"), number_format))

    def highlightBlock(self, text):
        for pattern, text_format in self.rules:
            for match in pattern.finditer(text):
                self.setFormat(match.start(), match.end() - match.start(), text_format)


app = QApplication(sys.argv)


app.setPalette(app.style().standardPalette())

window = QMainWindow()
window.setWindowTitle("Mobile IDE")
window.resize(440, 480)

"""

"""

current_file = None

editor = QTextEdit()
editor.setPlaceholderText("Write your code here...")

editor.setStyleSheet("""
    QTextEdit {
        background-color: black;
        color: white;
        font-family: Cascadia Code;
        
        border: none;
        padding: 5px;
        border: 2px groove grey;
    }
""")

output = QTextEdit()
output.setReadOnly(True)
output.setPlaceholderText("Program output...")

output.setStyleSheet("""
    QTextEdit {
        background-color: black;
        color: white;
        border: none;
        padding: 5px;
        border: 2px groove grey;
    }
""")

font_editor = QFont("Monospace", 16)

font_output = QFont("DejaVu Sans Mono", 16)


font_editor.setStyleHint(QFont.StyleHint.Monospace)

font_output.setStyleHint(QFont.StyleHint.Monospace)


editor.setFont(font_editor)
output.setFont(font_output)

highlighter = PythonHighlighter(editor.document())

highlighter = PythonHighlighter(output.document())


splitter = QSplitter(Qt.Orientation.Vertical)
splitter.addWidget(editor)
splitter.addWidget(output)
splitter.setSizes([300, 180])

container = QWidget()
layout = QVBoxLayout(container)
layout.setContentsMargins(2, 2, 2, 2)
layout.addWidget(splitter)

window.setCentralWidget(container)


def new_file():
    global current_file

    editor.clear()
    output.clear()
    current_file = None
    window.setWindowTitle("Mobile IDE")


def open_file():
    global current_file

    filename, _ = QFileDialog.getOpenFileName(
        window, "Open File", "test.py", "All Files (*)"
    )

    if filename:
        with open(filename, "r", encoding="utf-8") as file:
            editor.setPlainText(file.read())

        current_file = filename
        window.setWindowTitle(os.path.basename(filename))


def save_file():
    global current_file

    if current_file is None:
        save_file_as()
        return

    with open(current_file, "w", encoding="utf-8") as file:
        file.write(editor.toPlainText())


def save_file_as():
    global current_file

    filename, _ = QFileDialog.getSaveFileName(
        window, "Save File", "test.", "All Files (*)"
    )

    if filename:
        current_file = filename
        save_file()
        window.setWindowTitle(os.path.basename(filename))


def execute(command, source, suffix, link_command=None):
    output.clear()

    filename = None
    object_file = None
    executable = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=suffix, encoding="utf-8", delete=False
        ) as file:
            file.write(source)
            filename = file.name

        directory = os.path.dirname(filename)
        executable = os.path.join(directory, "mobile_program")

        if link_command:
            object_file = executable + ".o"

            compile_command = command + [filename, "-o", object_file]

            result = subprocess.run(
                compile_command, capture_output=True, text=True, timeout=30
            )

            if result.returncode != 0:
                output.setPlainText(result.stderr)
                return

            result = subprocess.run(
                link_command + [object_file, "-o", executable],
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode != 0:
                output.setPlainText(result.stderr)
                return

            run_command = [executable]

        else:
            run_command = command + [filename]

            if suffix in (".c", ".cpp"):
                compile_command = command + [filename, "-o", executable]

                result = subprocess.run(
                    compile_command, capture_output=True, text=True, timeout=30
                )

                if result.returncode != 0:
                    output.setPlainText(result.stderr)
                    return

                run_command = [executable]

        result = subprocess.run(run_command, capture_output=True, text=True, timeout=30)

        output.setPlainText(result.stdout + result.stderr)

        if result.returncode != 0:
            output.append(f"\nExit code: {result.returncode}")

    except subprocess.TimeoutExpired:
        output.setPlainText("Execution timed out.")

    except Exception as error:
        output.setPlainText(str(error))

    finally:
        for path in (filename, object_file, executable):
            if path and os.path.exists(path):
                os.unlink(path)


def run_python():
    execute([sys.executable], editor.toPlainText(), ".py")


def run_bash():
    execute(["sh", "-c"], editor.toPlainText(), ".sh")


def run_arm64():
    execute(["as"], editor.toPlainText(), ".s", ["ld", "-pie"])


def run_c():
    execute(["gcc"], editor.toPlainText(), ".c")


def run_cpp():
    execute(["g++"], editor.toPlainText(), ".cpp")


"""
file_menu = window.menuBar().addMenu("File")

file_actions = [
    ("New", new_file, "Ctrl+N"),
    ("Open", open_file, "Ctrl+O"),
    ("Save", save_file, "Ctrl+S"),
    ("Save As", save_file_as, "Ctrl+Shift+S"),
    ("Run Python", run_python, "F5"),
    ("Run C", run_c, ""),
    ("Run C++", run_cpp, ""),
    ("Run Bash", run_bash, ""),
    ("Run ARM64", run_arm64, ""),
    ("Exit", app.quit, "Ctrl+Q")
]

for name, function, shortcut in file_actions:
    action = QAction(name, window)
    action.triggered.connect(function)

    if shortcut:
        action.setShortcut(QKeySequence(shortcut))

    file_menu.addAction(action)


edit_menu = window.menuBar().addMenu("Edit")

edit_actions = [
    ("Undo", editor.undo, "Ctrl+Z"),
    ("Redo", editor.redo, "Ctrl+Y"),
    ("Cut", editor.cut, "Ctrl+X"),
    ("Copy", editor.copy, "Ctrl+C"),
    ("Paste", editor.paste, "Ctrl+V"),
    ("Select All", editor.selectAll, "Ctrl+A")
]

for name, function, shortcut in edit_actions:
    action = QAction(name, window)
    action.triggered.connect(function)
    action.setShortcut(QKeySequence(shortcut))
    edit_menu.addAction(action)

"""

toolbar = QToolBar()
window.addToolBar(toolbar)


new_action = QAction(
    window.style().standardIcon(QStyle.StandardPixmap.SP_DialogRetryButton), "✖", window
)

new_action.triggered.connect(new_file)

toolbar.addAction(new_action)


open_action = QAction(
    window.style().standardIcon(QStyle.StandardPixmap.SP_DialogOpenButton),
    "Open",
    window,
)

open_action.triggered.connect(open_file)

toolbar.addAction(open_action)


save_action = QAction(
    window.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton),
    "Save",
    window,
)

save_action.triggered.connect(save_file_as)

toolbar.addAction(save_action)

arm64_action = QAction(
    window.style().standardIcon(QStyle.StandardPixmap.SP_DialogRetryButton),
    "ARM64 >",
    window,
)

arm64_action.triggered.connect(run_arm64)

toolbar.addAction(arm64_action)


cpp_action = QAction(
    window.style().standardIcon(QStyle.StandardPixmap.SP_DialogRetryButton),
    "C++ >",
    window,
)

cpp_action.triggered.connect(run_cpp)

toolbar.addAction(cpp_action)

bash_action = QAction(
    window.style().standardIcon(QStyle.StandardPixmap.SP_DialogRetryButton),
    "Sh >",
    window,
)

bash_action.triggered.connect(run_bash)

toolbar.addAction(bash_action)


python_exec_action = QAction(
    window.style().standardIcon(QStyle.StandardPixmap.SP_DialogRetryButton),
    "P >",
    window,
)

python_exec_action.triggered.connect(run_python)


toolbar.addAction(python_exec_action)


window.show()

sys.exit(app.exec())
