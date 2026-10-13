import readline
import time
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style, merge_styles
from prompt_toolkit.styles.pygments import style_from_pygments_cls
from pygments.styles import get_style_by_name


python_words = [
    "abs", "all", "and", "any", "append", "as", "assert",
    "async", "await", "bin", "bool", "break", "bytes",
    "callable", "chr", "class", "clear", "continue",
    "def", "del", "dict", "dir", "divmod", "elif", "else",
    "enumerate", "eval", "except", "False", "filter",
    "finally", "float", "for", "format", "from", "get",
    "global", "hasattr", "help", "if", "import", "in",
    "input", "int", "is", "isinstance", "issubclass",
    "iter", "items", "keys", "lambda", "len", "list",
    "locals", "map", "max", "min", "next", "None",
    "null", "object", "open", "or", "ord", "pass",
    "print", "property", "range", "repr", "return", "reversed",
    "round", "set", "setattr", "slice", "sorted", "str",
    "sum", "super", "try", "tuple", "type", "update",
    "values", "vars", "while", "with", "yield", "zip"
]


python_dict = {
    "abs": ("Return the absolute value", "abs(-5)  # 5"),
    "all": ("Return True if all items are true", "all([True, True])"),
    "and": ("Require both conditions to be true", "if x > 0 and x < 10:"),
    "any": ("Return True if any item is true", "any([False, True])"),
    "append": ("Add an item to a list", "numbers.append(10)"),
    "as": ("Assign an alias or name in a with statement", "import math as m"),
    "assert": ("Raise an error if a condition is false", "assert x > 0"),
    "async": ("Define asynchronous code", "async def task():"),
    "await": ("Wait for an asynchronous operation", "await task()"),
    "bin": ("Convert an integer to binary text", "bin(10)  # '0b1010'"),
    "bool": ("Convert a value to True or False", "bool(1)  # True"),
    "break": ("Exit a loop immediately", "break"),
    "bytes": ("Create an immutable bytes object", "bytes([65, 66])"),
    "callable": ("Check whether an object can be called", "callable(print)"),
    "chr": ("Convert an integer to a character", "chr(65)  # 'A'"),
    "class": ("Define a class", "class Animal:"),
    "clear": ("Remove all items from a collection", "numbers.clear()"),
    "continue": ("Skip to the next loop iteration", "continue"),
    "def": ("Define a function", "def greet():"),
    "del": ("Delete a variable or item", "del numbers[0]"),
    "dict": ("Create a dictionary", "dict(name='Sam')"),
    "dir": ("List an object's available attributes", "dir(str)"),
    "divmod": ("Return quotient and remainder", "divmod(10, 3)  # (3, 1)"),
    "elif": ("Check another condition", "elif x == 0:"),
    "else": ("Run code when other conditions fail", "else:"),
    "enumerate": ("Loop with an index and value", "enumerate(['a', 'b'])"),
    "eval": ("Evaluate a Python expression from text", "eval('2 + 3')  # 5"),
    "except": ("Handle an exception", "except ValueError:"),
    "False": ("Boolean value representing false", "result = False"),
    "filter": ("Select items matching a condition", "filter(None, [0, 1, 2])"),
    "finally": ("Run code whether an exception occurs or not", "finally:"),
    "float": ("Convert a value to a floating-point number", "float('3.5')"),
    "for": ("Loop over items", "for item in numbers:"),
    "format": ("Format a value as text", "format(3.14, '.1f')"),
    "from": ("Import a name from a module", "from math import sqrt"),
    "get": ("Retrieve a dictionary value safely", "person.get('age', 0)"),
    "global": ("Refer to a global variable inside a function", "global count"),
    "hasattr": ("Check whether an object has an attribute", "hasattr(person, 'name')"),
    "help": ("Display Python help information", "help(str)"),
    "if": ("Run code when a condition is true", "if x > 0:"),
    "import": ("Import a module", "import math"),
    "in": ("Check membership or iterate over items", "if 'a' in text:"),
    "input": ("Read text entered by the user", "name = input('Name: ')"),
    "int": ("Convert a value to an integer", "int('42')"),
    "is": ("Check whether two references are identical", "if value is None:"),
    "isinstance": ("Check whether an object has a given type", "isinstance(5, int)"),
    "issubclass": ("Check whether one class inherits from another", "issubclass(bool, int)"),
    "iter": ("Create an iterator", "iterator = iter([1, 2, 3])"),
    "items": ("Return dictionary key-value pairs", "person.items()"),
    "keys": ("Return dictionary keys", "person.keys()"),
    "lambda": ("Create a small anonymous function", "square = lambda x: x * x"),
    "len": ("Return the number of items", "len('hello')  # 5"),
    "list": ("Create a list", "list((1, 2, 3))"),
    "locals": ("Return the current local namespace", "locals()"),
    "map": ("Apply a function to each item", "map(abs, [-1, 2, -3])"),
    "max": ("Return the largest item", "max(3, 8, 2)  # 8"),
    "min": ("Return the smallest item", "min(3, 8, 2)  # 2"),
    "next": ("Get the next item from an iterator", "next(iter([10, 20]))  # 10"),
    "None": ("Represent the absence of a value", "result = None"),
    "null": ("Not a Python keyword; JSON uses null", "value = None  # Python"),
    "object": ("Create or refer to the base object type", "isinstance(5, object)"),
    "open": ("Open a file", "file = open('data.txt', 'r')"),
    "or": ("Require at least one condition to be true", "if x < 0 or x > 10:"),
    "ord": ("Return a character's Unicode number", "ord('A')  # 65"),
    "pass": ("Do nothing; use as a placeholder", "def future_function(): pass"),
    "print": ("Display output", "print('Hello, world!')"),
    "property": ("Define a managed attribute in a class", "property(getter)"),
    "range": ("Generate a sequence of integers", "range(5)"),
    "repr": ("Return a developer-oriented representation", "repr('hello')"),
    "return": ("Return a value from a function", "return result"),
    "reversed": ("Iterate over items in reverse order", "list(reversed([1, 2, 3]))"),
    "round": ("Round a number", "round(3.14159, 2)  # 3.14"),
    "set": ("Create a set of unique items", "set([1, 1, 2])  # {1, 2}"),
    "setattr": ("Set an object's attribute", "setattr(person, 'age', 30)"),
    "slice": ("Create a slice object", "slice(1, 5, 2)"),
    "sorted": ("Return a sorted list", "sorted([3, 1, 2])"),
    "str": ("Convert a value to text", "str(123)  # '123'"),
    "sum": ("Add the items in an iterable", "sum([1, 2, 3])  # 6"),
    "super": ("Access methods from a parent class", "super().__init__()"),
    "try": ("Begin a block that may raise an exception", "try:"),
    "tuple": ("Create an immutable sequence", "tuple([1, 2, 3])"),
    "type": ("Return an object's type", "type(42)  # <class 'int'>"),
    "update": ("Add or replace dictionary entries", "person.update({'age': 30})"),
    "values": ("Return dictionary values", "person.values()"),
    "vars": ("Return an object's attribute dictionary", "vars(person)"),
    "while": ("Repeat code while a condition is true", "while count < 5:"),
    "with": ("Manage a resource using a context manager", "with open('data.txt') as file:"),
    "yield": ("Produce a value from a generator", "yield number"),
    "zip": ("Combine items from multiple iterables", "list(zip([1, 2], ['a', 'b']))"),
}


pygment_style = style_from_pygments_cls(get_style_by_name("paraiso-dark"))


completion_style = Style.from_dict({
    "prompt": "bold #ffa500",
    "": "#cccccc",
    "completion-menu.completion": "bg:#111155 #ffffff",
    "completion-menu.completion.current": "bg:#00aaaa #000000",
    "scrollbar.background": "bg:#88aaaa",
    "scrollbar.button": "bg:#222222",
})


style = merge_styles([
    pygment_style,
    completion_style
])


def get_completer():
    return WordCompleter(
        python_words,
        ignore_case=True
    )


def python_decode(instruction):
    instruction = instruction.strip().lower()

    if not instruction:
        return None

    instruction = instruction.split()[0]

    if instruction in python_dict:
        description, example = python_dict[instruction]
        return f"{description}\n\nExample:\n{example}"

    return "Word not found"


def main():
    print("Python3 Guide & Dictionary\n")
    print("Type & Learn.\n")
    
    print("Type exit to quit.\n")

    session = PromptSession(
        style=style,
        auto_suggest=AutoSuggestFromHistory()
    )

    while True:
        try:
            instruction = session.prompt(
                [("class:prompt", "\nPython3> ")],
                completer=get_completer()
            )

            instruction = instruction.strip()

            if instruction.lower() in ("exit", "quit"):
                break

            result = python_decode(instruction)

            if result:
                time.sleep(0.4)
                print(result)

        except (KeyboardInterrupt, EOFError):
            print()
            break

    print("Goodbye!")


if __name__ == "__main__":
    main()
    