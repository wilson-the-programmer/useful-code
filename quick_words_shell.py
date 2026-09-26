"""
Read:

To create a file with words:

--------------------------------------
1) In shell:

pip install nltk

pip install textblob


2) Create hidden file with approximately 50,000 words or approximately 490,335 bytes :

--------------------------------------

If you have nano editor:


nano wordnet_words_dl.py


----------------------------
Code:
----------------------------

import os
from nltk.corpus import wordnet


def create_word_list(filename, limit=50000):
    words = set()

    for synset in wordnet.all_synsets():
        for lemma in synset.lemmas():
            word = lemma.name().replace("_", " ").lower()

            if word.isalpha():
                words.add(word)

            if len(words) >= limit:
                break

        if len(words) >= limit:
            break

    words = sorted(words)

    with open(filename, "w", encoding="utf-8") as file:
        file.write("\n".join(words))


filename = os.path.expanduser("~/.wordnet_words")

create_word_list(filename)

print(f"Created {filename}")


3 ) creat another file ( Python ) like "quick_words.py'

nano quick_words.py


-------------------------------------
Code:
-------------------------------------


import readline
import os
from textblob import Word



ORANGE = "\033[1;38;2;255;165;0m"
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




4) Save & Exit nano or whatever editor that you use.

5) Test program:


$ python3 quick_words.py


Example:

Word: %def sun

the star that is the source of light and heat for the planets in the solar system

Word: %def star

(astronomy) a celestial body of hot gases that radiates energy derived from thermonuclear reactions in the interior

Word: %def science 

a particular branch of scientific knowledge

Word: 


"""




import readline
import os
from textblob import Word



ORANGE = "\033[1;38;2;255;165;0m"
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





