
from simple_term_menu import TerminalMenu
import os

current_directory = os.listdir()

programs = [
    filename
    for filename in current_directory
    if filename.endswith(".go") and filename != "quick_github.go"
]

if not programs:
    print("No Go programs found.")
    exit()

terminal_menu = TerminalMenu(programs)
choice = terminal_menu.show()

if choice is not None:
    selected_program = programs[choice]
    os.system(f"go run {selected_program}")

