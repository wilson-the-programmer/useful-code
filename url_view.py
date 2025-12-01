import requests
from bs4 import BeautifulSoup
import urllib.parse
import subprocess

BOLD_CYAN = "\033[1;36m"
BOLD_WHITE = "\033[1;37m"
RESET = "\033[0m"

last_url = ""

def get_real_url(ddg_url):
    parsed = urllib.parse.urlparse(ddg_url)
    qs = urllib.parse.parse_qs(parsed.query)
    if "uddg" in qs:
        return urllib.parse.unquote(qs["uddg"][0])
    return ddg_url

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

while True:
    uru = input(f"{BOLD_CYAN}\n\nURL: {RESET}").strip()
    if uru.lower() in {"exit", "quit"}:
        break

    # open last URL in browser via Termux
    if uru.lower() in {"open", "go", "visit"}:
        if last_url:
            open_url_in_termux(last_url)
            print(f"\nOpened {last_url} via Termux.\n")
        else:
            print("\nNo URL stored yet.\n")
        continue

    # detect if input looks like a URL
    if uru.startswith("http://") or uru.startswith("https://") or "." in uru:
        if not uru.startswith("http://") and not uru.startswith("https://"):
            uru = "https://" + uru
        last_url = uru
        content = fetch_full_page(last_url)
        print(f"\n{BOLD_WHITE}{content}{RESET}\n")
    else:
        # treat input as a DuckDuckGo search query
        query = urllib.parse.quote(uru)
        search_url = f"https://duckduckgo.com/?q={query}"
        open_url_in_termux(search_url)
        print(f"\nOpened DuckDuckGo search for '{uru}' via Termux.\n")
        
        
        