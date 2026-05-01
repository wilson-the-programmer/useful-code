from textblob import Word
import readline
import shutil
import textwrap
import time

ORANGE = "\033[1;38;2;255;165;0m"
LIGHT_BLUE = "\033[1;38;2;173;216;230m"
LIGHT_GREY = "\033[1;38;2;200;200;200m"
RESET = "\033[0m"

with open("words.txt", "r", encoding="utf-8") as f:
    WORD_LIST = [line.strip() for line in f if line.strip()]

def search_words(prefix, min_len=1, limit=50):
    prefix = prefix.lower()
    results = []

    for w in WORD_LIST:
        lw = w.lower()

        if lw.startswith(prefix) and len(w) >= min_len:
            results.append(w)

        if len(results) == limit:
            break

    return results

while True:
    searched_word = input(
        f"\n{ORANGE}Word {LIGHT_BLUE}(or type 'exit' to quit)\n"
        f"{ORANGE}or 'words: text, min_len'\n\n{LIGHT_GREY}"
    ).strip()

    print(RESET, end="")

    if searched_word.lower() == "exit":
        break

    if not searched_word:
        continue

    if searched_word.lower().startswith("words:"):
        query = searched_word[6:].strip()

        if "," in query:
            parts = query.split(",", 1)
            prefix = parts[0].strip()
            try:
                min_len = int(parts[1].strip())
            except:
                min_len = 1
        else:
            prefix = query.strip()
            min_len = 1

        matches = search_words(prefix, min_len=min_len, limit=50)

        if matches:
            print(f"\n{ORANGE}Matches for '{prefix}' (min {min_len} chars):{RESET}\n")
            time.sleep(0.4)

            for w in matches:
                print(f"{LIGHT_GREY}• {w}{RESET}")
                time.sleep(0.03)
        else:
            print(f"{LIGHT_GREY}No matches found.{RESET}")

        continue

    width = shutil.get_terminal_size().columns
    wrap_width = max(20, width - 4)

    word = Word(searched_word)
    definitions = word.definitions

    if definitions:
        print(f"\n{ORANGE}Definitions for '{searched_word}':{RESET}\n")
        time.sleep(0.8)

        for d in definitions:
            d = d.strip()

            if d:
                d = d[0].upper() + d[1:]

                if not d.endswith("."):
                    d += "."

                wrapped = textwrap.fill(d, width=wrap_width)
                lines = wrapped.split("\n")

                print(f"{LIGHT_GREY}• {lines[0]}{RESET}")

                for line in lines[1:]:
                    print(f"{LIGHT_GREY}  {line}{RESET}")

                print(f"{LIGHT_GREY}--------------------{RESET}")
                time.sleep(0.15)
    else:
        print(f"{LIGHT_GREY}No definitio
ns found for '{searched_word}'.{RESET}")

