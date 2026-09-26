
import os
from textblob import Word
import readline


GREY = "\033[1;38;210;210;210m"
ORANGE = "\033[1;38;255;265;0m"
RESET = "\033[0m"


def load_words():
    filename = os.path.expanduser("~/.wordnet_words")

    with open(filename, encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]


words = load_words()


def generate_words(prefix, limit=20):
    prefix = prefix.lower()

    matches = [
        word for word in words
        if word.startswith(prefix)
    ]

    return matches[:limit]


def define_word(word):
    meanings = Word(word).definitions

    if not meanings:
        return "No definition found."

    return meanings[0]


while True:
    command = input(f"{ORANGE}Word: {RESET}").strip()

    if command == "q" or command == "exit":
        break

    if command.startswith("%def "):
        word = command[5:].strip()

        if word:
            print()
            print(define_word(word))
            print()
        continue

    print()

    for word in generate_words(command):
        print(word)

    print()

