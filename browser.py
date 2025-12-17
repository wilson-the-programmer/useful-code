
import requests
import os
from bs4 import BeautifulSoup
import urllib.parse
import subprocess
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.styles import Style

BOLD_ORANGE = "\033[1;38;5;208m"
BOLD_YELLOW = "\033[1;33m"
BOLD_BEIGE = "\033[1;37m"
SOFT_BROWN = "\033[38;5;173m"
OFF_WHITE = "\033[38;5;230m"
SEPARATOR_BROWN = "\033[38;5;180m"
INDEX_YELLOW = "\033[38;5;226m"
WARNING_ORANGE = "\033[38;5;214m"
BOLD_WHITE = "\033[1;37m"
BOLD_CYAN = "\033[1;36m"
RESET = "\033[0m"

HISTORY_FILE = "search_history.txt"
BLOCKED_DOMAINS = ["cnn.com", "nytimes.com", "msnbc.com", "theguardian.com", "huffpost.com"]

style = Style.from_dict({'prompt': 'bold #00ffff'})
session = PromptSession(history=FileHistory(HISTORY_FILE), auto_suggest=AutoSuggestFromHistory())

last_url = ""

def fetch_full_page(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=5)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()
        elements = soup.find_all(["h1", "h2", "h3", "p"])
        text = "\n\n".join(e.get_text().strip() for e in elements if e.get_text().strip())
        return text if text else "No content found."
    except Exception as e:
        return f"Error fetching page: {e}"

def open_url_in_termux(url):
    subprocess.run(["termux-open-url", url])

def get_snippet(url, paragraphs=3):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(resp.text, "html.parser")
        ps = soup.find_all("p")
        snippet = "\n\n".join([p.get_text() for p in ps[:paragraphs]])
        return snippet.strip() if snippet else "[No preview available]"
    except Exception:
        return "[Could not fetch preview]"

while True:
    try:
        query = session.prompt([('class:prompt', '\n\nSearch: ')], style=style)
    except (KeyboardInterrupt, EOFError):
        break

    if query.lower() == "exit" or query.lower() == "q":
        break
        
    if query.lower() == "sys":
        while True:
        	command = session.prompt([('class:prompt', '\n$ ')])
        	os.system(f"{command}")
        	
        	if command == "exit":
        		break
        		        

    # URL mode: print full page if user types 'url <link>'
    if query.lower().startswith("url "):
        url = query[4:].strip()
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        last_url = url
        content = fetch_full_page(url)
        print(f"\n{BOLD_WHITE}{content}{RESET}\n")
        continue

    # Search mode: normal DuckDuckGo search
    search_url = f"https://duckduckgo.com/html/?q={urllib.parse.quote_plus(query)}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        resp = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(resp.text, "html.parser")
        results = soup.find_all("a", class_="result__a", limit=6)

        if not results:
            print(f"{WARNING_ORANGE}No results found.{RESET}")
            continue

        for i, r in enumerate(results, 1):
            title = r.get_text()
            link = r['href']
            if "uddg=" in link:
                parsed = urllib.parse.parse_qs(urllib.parse.urlparse(link).query)
                link = parsed.get("uddg", [link])[0]

            if any(domain in link for domain in BLOCKED_DOMAINS):
                continue

            print(f"\n{INDEX_YELLOW}{i}. {SOFT_BROWN}{title}{RESET}")
            print(f"{BOLD_BEIGE}{link}{RESET}\n")

            preview = get_snippet(link)
            print(f"{OFF_WHITE}{preview}{RESET}")
            print(f"{SEPARATOR_BROWN}{'-'*30}{RESET}")

    except Exception as e:
        print(f"{WARNING_ORANGE}Error fetching results:{RESET}", e)