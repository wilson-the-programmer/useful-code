# Awesome Tkinter GUI app 


import io
from io import BytesIO

import os
import random
import re
import subprocess
import sys
import tempfile
import threading
import traceback
import keyword
import urllib.parse

import webbrowser
import textwrap

#import xml.etree.ElementTree

from xml.etree import ElementTree

# tree = ElementTree.fromstring(response.content)


import tkinter as tk
from tkinter import (
    scrolledtext,
    simpledialog,
    colorchooser,
    filedialog,
    messagebox,
    Menu,
    ttk,
)
from tkinter.font import families

# 3rd party libraries

import requests

from bs4 import BeautifulSoup

import black



# this comes with Python3 but is technically 3rd party
from jnius import autoclass

cpp_keywords = [
    "alignas",
    "alignof",
    "and",
    "and_eq",
    "asm",
    "auto",
    "bitand",
    "bitor",
    "bool",
    "break",
    "case",
    "catch",
    "char",
    "char8_t",
    "char16_t",
    "char32_t",
    "class",
    "compl",
    "const",
    "consteval",
    "constexpr",
    "const_cast",
    "continue",
    "decltype",
    "default",
    "delete",
    "do",
    "double",
    "dynamic_cast",
    "else",
    "enum",
    "explicit",
    "export",
    "extern",
    "false",
    "float",
    "for",
    "friend",
    "goto",
    "if",
    "inline",
    "int",
    "long",
    "mutable",
    "namespace",
    "new",
    "noexcept",
    "not",
    "not_eq",
    "nullptr",
    "operator",
    "or",
    "or_eq",
    "private",
    "protected",
    "public",
    "register",
    "reinterpret_cast",
    "return",
    "short",
    "signed",
    "sizeof",
    "static",
    "static_assert",
    "static_cast",
    "struct",
    "switch",
    "template",
    "this",
    "thread_local",
    "throw",
    "true",
    "try",
    "typedef",
    "typeid",
    "typename",
    "union",
    "unsigned",
    "using",
    "virtual",
    "void",
    "volatile",
    "wchar_t",
    "while",
    "xor",
    "xor_eq",
    #python
    "print",
    "(",
    ")"
    "+",
    "-",
    "/",
    "*"
    
]




last_opened_link = ""
font_style = "Noto Sans Mono CJK JP"


def web_browser():
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
            text = "\n\n".join(
                e.get_text().strip() for e in elements if e.get_text().strip()
            )
            return text if text else "No content found."
        except Exception as e:
            return f"Error fetching page: {e}"

    def search_and_extract_links(query):
        blocked_domains = [
            "reuters.com",
            "news.google.com",
            "msnbc.com",
            "msn.com",
            "nbcnews.com",
            "nytimes.com",
            "washingtonpost.com",
            "theguardian.com",
            "politico.com",
            "vox.com",
            "huffpost.com",
            "theatlantic.com",
            "slate.com",
            "newyorker.com",
            "buzzfeednews.com",
            "motherjones.com",
            "npr.org",
            "usnews.com",
            "thehill.com",
            "marketwatch.com",
            "youtube.com",
            "twitter.com",
        ]
        query_encoded = urllib.parse.quote(query)
        search_url = f"https://html.duckduckgo.com/html/?q={query_encoded}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(search_url, headers=headers, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find_all("a", class_="result__a")[:15]
        extracted = []
        for link in results:
            title = link.get_text().strip()
            ddg_link = link.get("href")
            real_link = get_real_url(ddg_link)
            domain = urllib.parse.urlparse(real_link).netloc.replace("www.", "")
            if domain in blocked_domains:
                continue
            extracted.append((title, real_link))
            if len(extracted) >= 4:
                break
        return extracted

    def get_domain(url):
        try:
            parsed = urllib.parse.urlparse(url)
            return parsed.netloc.replace("www.", "")
        except:
            return url

    def search_and_display_links():
        query = entry.get("insert linestart", "insert lineend").strip()
        if not query:
            return
        try:
            results = search_and_extract_links(query)
        except Exception as e:
            results = []
            print(f"Error fetching search results: {e}")
        for widget in link_frame.winfo_children():
            widget.destroy()
        # Make link_frame visible and shrink the webpage_viewer
        link_frame.pack(padx=5, pady=10, fill=tk.BOTH, expand=False)
        webpage_viewer.pack_forget()
        webpage_viewer.pack(
            padx=0, pady=0, fill=tk.BOTH, expand=True, side=tk.BOTTOM, ipadx=0, ipady=0
        )
        for title, link in results:
            top_line = " ".join(title.split()[:5])
            bottom_line = get_domain(link)
            button_text = f"{top_line}\n{bottom_line}"
            btn_link = tk.Button(
                link_frame,
                text=button_text,
                font=("Courier New", 8),
                cursor="hand2",
                height=2,
                wraplength=650,
                anchor="w",
                justify="left",
                padx=5,
                pady=5,
                bg=random_light_color(),
                command=lambda url=link: open_link_in_viewer(url),
            )
            btn_link.pack(fill=tk.X, padx=5, pady=3)

    def open_link_in_viewer(url):
        global last_opened_link
        last_opened_link = url
        content = fetch_full_page(url)
        webpage_viewer.config(state=tk.NORMAL)
        webpage_viewer.delete("1.0", tk.END)
        webpage_viewer.insert(tk.END, content)
        webpage_viewer.config(state=tk.DISABLED)

    def clear_links():
        for widget in link_frame.winfo_children():
            widget.destroy()
        link_frame.pack_forget()
        webpage_viewer.pack_forget()
        webpage_viewer.pack(padx=0, pady=0, fill=tk.BOTH, expand=True, side=tk.BOTTOM)

    def view_webpage_typed():
        global last_opened_link
        try:
            url = entry.get(1.0, "end").strip()
            if not url.startswith("https://"):
                url = "https://" + url
        except:
            pass
        last_opened_link = url
        content = fetch_full_page(url)
        webpage_viewer.config(state=tk.NORMAL)
        webpage_viewer.delete("1.0", tk.END)
        webpage_viewer.insert(tk.END, content)
        webpage_viewer.config(state=tk.DISABLED)

    def random_light_color():
        r = random.randint(180, 250)
        g = random.randint(180, 250)
        b = random.randint(180, 250)
        return f"#{r:02x}{g:02x}{b:02x}"

    def paste_last_link():
        if last_opened_link:
            entry.delete("1.0", tk.END)
            entry.insert(tk.END, last_opened_link)
        else:
            messagebox.showinfo("No Link", "No link has been clicked yet.")

    def save_page():
        content = webpage_viewer.get("1.0", tk.END)
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("Saved", f"Page saved to {file_path}")

    def copy_selected():
        try:
            current_widget = browser_root.focus_get()
            selected = current_widget.selection_get()
            browser_root.clipboard_clear()
            browser_root.clipboard_append(selected)
        except tk.TclError:
            messagebox.showwarning("Copy", "No text selected!")

    def search_selected():
        try:
            selected = webpage_viewer.selection_get()
            query = urllib.parse.quote(selected)
            webbrowser.open_new_tab(f"https://google.com/search?q={query}")
        except tk.TclError:
            messagebox.showwarning("Search", "No text selected!")

    def invert_screen():
        back = webpage_viewer.cget("background")
        fore = webpage_viewer.cget("foreground")
        webpage_viewer.config(bg=fore, fg=back)

    def random_dark_screen():
        dark_bg = "#{:02x}{:02x}{:02x}".format(
            random.randint(0, 70), random.randint(0, 70), random.randint(0, 70)
        )
        light_fg = "#{:02x}{:02x}{:02x}".format(
            random.randint(175, 255), random.randint(175, 255), random.randint(175, 255)
        )
        webpage_viewer.config(bg=dark_bg, fg=light_fg)
        entry.delete(1.0, "end")
        entry.insert(1.0, f"bg={dark_bg}\nfg={light_fg}")

    def clear_widget():
        entry.delete(1.0, "end")

    def view_page_with_chrome():
        try:
            webbrowser.open_new_tab(last_opened_link)
        except:
            pass

    DELAY = 100
    MAX_LINES = 6

    def get_google_autocomplete(query):
        if not query.strip():
            return []
        url = f"https://suggestqueries.google.com/complete/search?output=toolbar&q={query}"
        try:
            response = requests.get(url)
            suggestions = []
            if response.status_code == 200:
                tree = ElementTree.fromstring(response.content)
                for elem in tree.iter("suggestion"):
                    suggestions.append(elem.attrib["data"])
            return suggestions[:MAX_LINES]
        except:
            return []

    def fetch_suggestions():
        typed_text = entry.get("insert linestart", "insert lineend")
        suggestions = get_google_autocomplete(typed_text) if typed_text.strip() else []
        browser_root.after(0, lambda: update_suggestions(suggestions))

    def update_suggestions(suggestions):
        cursor = entry.index(tk.INSERT)
        current_line_end = entry.index("insert lineend")
        next_line = current_line_end + " +1c"
        entry.delete(next_line, next_line + f" +{MAX_LINES}lines")
        if suggestions:
            entry.insert(next_line, "\n" + "\n".join(suggestions))
        entry.mark_set(tk.INSERT, cursor)

    fetch_job = None

    def schedule_fetch(event):
        nonlocal fetch_job
        if fetch_job is not None:
            browser_root.after_cancel(fetch_job)
        fetch_job = browser_root.after(
            DELAY,
            lambda: threading.Thread(target=fetch_suggestions, daemon=True).start(),
        )

    # try: Droid Sans Mono, Source Sans Pro SemiBold, Roboto, Cutive Mono
    def change_font_style():
        current_widget = browser_root.focus_get()
        style = simpledialog.askstring("Font", "Style Name?").strip()
        try:
            current_widget.config(font=(style, 9))
        except:
            pass

    def google_search():
        query = (
            entry.get("insert linestart", "insert lineend").strip().replace(" ", "+")
        )
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open_new_tab(url)

    def duckduckgo_search():
        query = (
            entry.get("insert linestart", "insert lineend").strip().replace(" ", "+")
        )
        url = f"https://duckduckgo.com/?q={query}"
        webbrowser.open_new_tab(url)

    def youtube_search():
        query = (
            entry.get("insert linestart", "insert lineend").strip().replace(" ", "+")
        )
        url = f"https://www.youtube.com/results?search_query={query}"
        webbrowser.open_new_tab(url)

    def image_search():
        query = (
            entry.get("insert linestart", "insert lineend").strip().replace(" ", "+")
        )
        url = f"https://duckduckgo.com/?q={query}&iax=images&ia=images"
        webbrowser.open_new_tab(url)

    def google_image_search():
        query = (
            entry.get("insert linestart", "insert lineend").strip().replace(" ", "+")
        )
        url = f"https://www.google.com/search?q={query}&tbm=isch"
        webbrowser.open_new_tab(url)

    def google_news_search():
        query = (
            entry.get("insert linestart", "insert lineend").strip().replace(" ", "+")
        )
        url = f"https://news.google.com/search?q={query}"
        webbrowser.open_new_tab(url)

    def select_all_text():
        webpage_viewer.tag_add("sel", "1.0", "end-1c")

    browser_root = tk.Toplevel(root)
    browser_root.title("Web Browser")
    browser_root.geometry("460x740+0+0")
    browser_root.config(bg="white")
    menu_bar = tk.Menu(browser_root, font=("Courier New", 10), bd=3, bg="white")
    browser_root.config(menu=menu_bar)
    option_menu = tk.Menu(
        menu_bar,
        tearoff=0,
        font=("Courier New", 10),
        bd=2,
        bg="lightcyan",
        fg="darkblue",
    )
    menu_bar.add_cascade(label="Options", menu=option_menu)
    option_menu.add_command(
        label="Edit Mode", command=lambda: webpage_viewer.config(state=tk.NORMAL)
    )
    option_menu.add_command(
        label="Read-Only Mode", command=lambda: webpage_viewer.config(state=tk.DISABLED)
    )
    option_menu.add_command(label="Save Page As...", command=save_page)
    option_menu.add_command(label="Select All", command=select_all_text)
    option_menu.add_command(label="Copy Selected", command=copy_selected)
    option_menu.add_command(
        label="Paste", command=lambda: entry.event_generate("<<Paste>>")
    )
    option_menu.add_command(label="Clear Links/Expand View", command=clear_links)
    option_menu.add_command(label="Clear Page", command=clear_widget)
    option_menu.add_command(label="Font Style", command=change_font_style)
    option_menu.add_command(label="Paste Last Clicked Link", command=paste_last_link)
    option_menu.add_command(label="Exit", command=browser_root.destroy)
    dev_menu = tk.Menu(
        menu_bar,
        tearoff=0,
        font=("Courier New", 10),
        bd=2,
        bg="lightcyan",
        fg="darkblue",
    )
    menu_bar.add_cascade(label="Dev", menu=dev_menu)
    dev_menu.add_command(label="Dark Screen", command=random_dark_screen)
    dev_menu.add_command(label="Invert Screen", command=invert_screen)
    web_menu = tk.Menu(
        menu_bar, tearoff=0, font=("Courier New", 10), bd=2, bg="white", fg="blue"
    )
    menu_bar.add_cascade(label="Web", menu=web_menu)
    web_menu.add_command(label="Google News", command=google_news_search)
    web_menu.add_command(label="Google", command=google_search)
    web_menu.add_command(label="Google Images", command=google_image_search)
    web_menu.add_command(label="DuckDuckGo Search", command=duckduckgo_search)
    web_menu.add_command(label="DuckDuckGo Images", command=image_search)
    web_menu.add_command(label="YouTube", command=youtube_search)
    web_menu.add_command(label="Open Chrome (selected)", command=search_selected)
    web_menu.add_command(label="URL via Chrome", command=view_page_with_chrome)
    web_menu.add_command(label="View WebPage", command=view_webpage_typed)
    entry = tk.scrolledtext.ScrolledText(
        browser_root,
        width=40,
        height=4,
        font=("Courier New", 8),
        bg="black",
        fg="white",
        padx=10,
        pady=6,
        bd=2,
        insertbackground="orange",
        insertwidth=5,
    )
    entry.focus_set()
    entry.pack(padx=0, pady=0)
    button_frame = tk.Frame(browser_root)
    button_frame.pack(pady=5)
    clear_button = tk.Button(
        button_frame,
        text="Clear",
        width=2,
        bg="#550000",
        fg="red",
        command=clear_widget,
        font=("Courier New", 9),
        relief="raised",
        bd=2,
    )
    clear_button.pack(side=tk.LEFT, padx=2, pady=2)
    url_button = tk.Button(
        button_frame,
        text="Link",
        width=2,
        bg="gold",
        command=lambda: (entry.delete(1.0, "end"), paste_last_link()),
        font=("Courier New", 9),
        relief="raised",
        bd=2,
    )
    url_button.pack(side=tk.LEFT, padx=2, pady=2)
    copy_button = tk.Button(
        button_frame,
        text="Copy",
        width=2,
        bg="lightcyan",
        command=copy_selected,
        font=("Courier New", 9),
        relief="raised",
        bd=2,
    )
    copy_button.pack(side=tk.LEFT, padx=2, pady=2)
    expand_button = tk.Button(
        button_frame,
        text="[]",
        width=2,
        bg="orange",
        command=clear_links,
        font=("Courier New", 9),
        relief="raised",
        bd=2,
    )
    expand_button.pack(side=tk.LEFT, padx=2, pady=2)
    search_button = tk.Button(
        button_frame,
        text="Search",
        width=3,
        bg="black",
        fg="orange",
        command=search_and_display_links,
        font=("Times", 9, "bold"),
        relief="raised",
        bd=2,
    )
    search_button.pack(side=tk.LEFT, padx=2, pady=2)
    link_frame = tk.Frame(browser_root)
    link_frame.pack(padx=5, pady=10, fill=tk.BOTH, expand=False)
    webpage_viewer = scrolledtext.ScrolledText(
        browser_root,
        width=40,
        height=9,
        wrap=tk.WORD,
        bg="#000000",
        fg="#e6f3e7",
        font=("Courier New", 8),
        padx=10,
        pady=10,
        bd=5,
        insertbackground="orange",
        insertwidth=5,
    )
    webpage_viewer.pack(padx=0, pady=0, fill=tk.BOTH, expand=True, side=tk.BOTTOM)

    entry.bind("<KeyRelease>", schedule_fetch)
    browser_root.mainloop()


def clear_window():
    current_window = root.focus_get()
    current_window.delete("1.0", tk.END)


def clear_output():
    bottom_window.delete(1.0, "end")


def write_output(text):
    clear_output()

    bottom_window.insert(tk.END, text)


def get_current_widget():
    w = root.focus_get()
    if w is None:
        return top_window
    return w


def run_flake8():
    def task():
        try:
            code = top_window.get("1.0", "end-1c")

            f = tempfile.NamedTemporaryFile(
                delete=False, suffix=".py", mode="w", encoding="utf-8"
            )
            f.write(code)
            f.close()

            result = subprocess.run(["flake8", f.name], capture_output=True, text=True)

            bottom_window.delete("1.0", "end")

            if result.stdout.strip():
                bottom_window.insert("end", result.stdout)
            elif result.stderr.strip():
                bottom_window.insert("end", result.stderr)
            else:
                bottom_window.insert("end", "No issues found")

            os.unlink(f.name)

        except:
            pass

    threading.Thread(target=task, daemon=True).start()


def run_python():
    current_widget = root.focus_get()
    code = current_widget.get(1.0, tk.END)
    output = io.StringIO()
    sys.stdout = output
    try:
        exec(code)

    except Exception as e:
        output.write(f"{type(e).__name__}: {e}")

    finally:
        sys.stdout = sys.__stdout__
        result = output.getvalue()
        bottom_window.delete(1.0, tk.END)
        bottom_window.insert(1.0, result)


def compile_run_c():
    def task():
        try:
            code = top_window.get("1.0", "end-1c")

            f = tempfile.NamedTemporaryFile(
                delete=False, suffix=".c", mode="w", encoding="utf-8"
            )
            f.write(code)
            f.close()

            exe = f.name + ".out"

            try:
                c = subprocess.run(
                    ["gcc", f.name, "-o", exe], capture_output=True, text=True
                )

                if c.returncode != 0:
                    write_output(c.stderr)
                    return

                r = subprocess.run([exe], capture_output=True, text=True)
                write_output(r.stdout + r.stderr)

            finally:
                if os.path.exists(f.name):
                    os.unlink(f.name)
                if os.path.exists(exe):
                    os.unlink(exe)

        except:
            pass

    threading.Thread(target=task, daemon=True).start()


def compile_run_cpp():
    def task():
        try:
            code = top_window.get("1.0", "end-1c")

            f = tempfile.NamedTemporaryFile(
                delete=False, suffix=".cpp", mode="w", encoding="utf-8"
            )
            f.write(code)
            f.close()

            exe = f.name + ".out"

            try:
                c = subprocess.run(
                    ["g++", f.name, "-o", exe], capture_output=True, text=True
                )

                if c.returncode != 0:
                    write_output(c.stderr)
                    return

                r = subprocess.run([exe], capture_output=True, text=True)
                write_output(r.stdout + r.stderr)

            finally:
                if os.path.exists(f.name):
                    os.unlink(f.name)
                if os.path.exists(exe):
                    os.unlink(exe)

        except:
            pass

    threading.Thread(target=task, daemon=True).start()


unix_words = [
    "ls",
    "cat",
    "cp",
    "mv",
    "rm",
    "mkdir",
    "rmdir",
    "pwd",
    "cd",
    "echo",
    "touch",
    "clear",
    "whoami",
    "date",
    "cal",
    "grep",
    "find",
    "sort",
    "wc",
    "head",
    "tail",
    "less",
    "more",
    "gcc",
    "g++",
    "python",
    "python3",
    "flake8",
    "cpplint",
    "clang",
    "clang++",
    "git",
    "make",
    "cmake",
    "ps",
    "top",
    "kill",
    "chmod",
    "chown",
]


def detect_command(event=None):
    current_window = root.focus_get()
    cmd = current_window.get("insert linestart", "insert lineend").strip()
    for c in unix_words:
        if c in cmd:
            run_command()
            current_window.event_generate("return")


def run_command():
    current_window = root.focus_get()
    cmd = current_window.get("insert linestart", "insert lineend").strip()
    if not cmd:
        return
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    write_output(r.stdout + r.stderr)


"""
This global variable is so that the run_cpp_exe function knows the last successful compiled C++ file.
"""
cpp_exe_path = None


def compile_cpp():
    def task():
        global cpp_exe_path
        try:
            code = top_window.get("1.0", "end-1c")

            f = tempfile.NamedTemporaryFile(
                delete=False, suffix=".cpp", mode="w", encoding="utf-8"
            )
            f.write(code)
            f.close()

            exe = f.name + ".out"

            c = subprocess.run(
                ["g++", f.name, "-o", exe], capture_output=True, text=True
            )

            if c.returncode != 0:
                write_output(c.stderr)
                if os.path.exists(f.name):
                    os.unlink(f.name)
                return

            cpp_exe_path = exe
            write_output("Compilation successful")

            if os.path.exists(f.name):
                os.unlink(f.name)

        except:
            pass

    threading.Thread(target=task, daemon=True).start()


def exe_cpp():
    def task():
        global cpp_exe_path
        try:
            if not cpp_exe_path or not os.path.exists(cpp_exe_path):
                write_output("No compiled executable found")
                return

            r = subprocess.run([cpp_exe_path], capture_output=True, text=True)
            write_output(r.stdout + r.stderr)

        except:
            pass

    threading.Thread(target=task, daemon=True).start()


def run_cpplint():
    def task():
        try:
            code = top_window.get("1.0", "end-1c")

            f = tempfile.NamedTemporaryFile(
                delete=False, suffix=".cpp", mode="w", encoding="utf-8"
            )
            f.write(code)
            f.close()

            result = subprocess.run(["cpplint", f.name], capture_output=True, text=True)

            bottom_window.delete("1.0", "end")

            output = result.stdout.strip() + "\n" + result.stderr.strip()
            output = output.strip()

            if output:
                bottom_window.insert("end", output)
            else:
                bottom_window.insert("end", "No issues found")

            os.unlink(f.name)

        except:
            pass

    threading.Thread(target=task, daemon=True).start()


def new_file():
    current_window = root.focus_get()
    current_window.delete("1.0", tk.END)
    current_window.delete("1.0", tk.END)


def open_file():
    current_widget = root.focus_get()

    file_path = filedialog.askopenfilename(
        filetypes=[
            ("Python", "*.py*"),
            ("C", "*.c"),
            ("C++", "*.cpp"),
            ("Text", "*.txt"),
        ]
    )

    if file_path:
        with open(file_path, "r") as file:
            content = file.read()
            current_widget.delete("1.0", tk.END)
            current_widget.insert(tk.INSERT, f"\n{content}")


def open_file_from_cursor():
    current_window = root.focus_get()
    try:
        file = current_window.get("insert linestart", "insert lineend").strip()
        if not file:
            return
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
        current_window.delete("1.0", tk.END)
        current_window.insert(tk.END, content)
    except:
        pass


def save_file():
    current_window = root.focus_get()
    p = filedialog.asksaveasfilename()
    if not p:
        return
    with open(p, "w", encoding="utf-8") as f:
        f.write(current_window.get("1.0", "end-1c"))


def set_bg():
    w = get_current_widget()
    c = colorchooser.askcolor()[1]
    if c:
        w.config(bg=c)


def set_fg():
    w = get_current_widget()
    c = colorchooser.askcolor()[1]
    if c:
        w.config(fg=c)


def set_cursor():
    w = get_current_widget()
    c = colorchooser.askcolor()[1]
    if c:
        w.config(insertbackground=c)


def set_font_size():
    w = get_current_widget()
    size = tk.simpledialog.askinteger("Font Size", "Enter size")
    if size:
        current = font.Font(font=w["font"])
        w.config(font=(current.actual("family"), size))


def clear_widget():
    w = get_current_widget()
    w.delete("1.0", tk.END)


def search_word():
    current_window = root.focus_get()

    try:
        word = simpledialog.askstring("Search", "Enter search text:")

        if not word:
            return

        start_pos = current_window.index("insert")

        pos = current_window.search(word, start_pos, stopindex="end")

        if pos:
            end_pos = f"{pos}+{len(word)}c"

            current_window.mark_set("insert", end_pos)
            current_window.see(end_pos)
            current_window.focus_set()

    except:
        pass


def select_all_text():
    try:
        current_window = root.focus_get()
        current_window.tag_add("sel", "1.0", "end")
    except:
        pass


def copy_text():
    try:
        current_window = root.focus_get()
        text = current_window.get("sel.first", "sel.last")

        root.clipboard_clear()
        root.clipboard_append(text)
    except:
        pass


def cut_text():
    try:
        current_window = root.focus_get()
        text = current_window.get("sel.first", "sel.last")

        root.clipboard_clear()
        root.clipboard_append(text)

        current_window.delete("sel.first", "sel.last")
    except:
        pass


def paste_text():
    try:
        current_window = root.focus_get()

        try:
            current_window.delete("sel.first", "sel.last")
        except:
            pass

        current_window.insert("insert", root.clipboard_get())
    except:
        pass


highlight_enabled = False


def remove_highlights():
    global highlight_enabled

    highlight_enabled = False

    if not highlight_enabled:
        top_window.tag_remove("kw", "1.0", "end")






def format_flake8():
    try:
        current_window = root.focus_get()

        text = current_window.get("1.0", "end")

        lines = text.splitlines()

        grouped = {}

        for line in lines:
            m = re.search(r"(.+?):(\d+):(\d+):\s+([A-Z]\d+)\s+(.*)", line)

            if not m:
                continue

            filename = m.group(1)
            line_number = int(m.group(2))
            message = f"{m.group(4)} {m.group(5)}"

            grouped.setdefault(line_number, []).append(message)

        output = []

        output.append(f"File: '{filename}'")
        output.append(f"Imperfections: {sum(len(v) for v in grouped.values())}")
        output.append("")

        for line_number in sorted(grouped):
            output.append(f"Line {line_number}:")
            output.append("")

            for msg in grouped[line_number]:
                output.append(f"• {msg}")

            output.append("")

        current_window.delete("1.0", "end")
        current_window.insert("1.0", "\n".join(output))

    except:
        pass


def format_cpplint():
    try:
        current_window = root.focus_get()

        text = current_window.get("1.0", "end")

        grouped = {}
        filename = "Unknown"
        total = 0

        for line in text.splitlines():

            if line.startswith("Total errors found:"):
                try:
                    total = int(line.split(":")[1].strip())
                except:
                    pass
                continue

            m = re.search(r"(.+?):(\d+):\s+(.*?)\s+\[([^\]]+)\]\s+\[(\d+)\]", line)

            if not m:
                continue

            filename = m.group(1)
            line_number = int(m.group(2))
            message = m.group(3)
            category = m.group(4)

            grouped.setdefault(line_number, []).append(f"{message} [{category}]")

        output = []

        output.append(f"File: '{filename}'")
        output.append(f"Imperfections: {total}")
        output.append("")

        for line_number in sorted(grouped):
            output.append(f"Line {line_number}:")
            output.append("")

            for msg in grouped[line_number]:
                output.append(f"• {msg}")

            output.append("")

        current_window.delete("1.0", "end")
        current_window.insert("1.0", "\n".join(output))

    except:
        pass




def list_functions():
    try:
        text = top_window.get("1.0", "end-1c")

        pattern = re.compile(r"^\s*def\s+([a-zA-Z_]\w*)\s*\(")

        bottom_window.delete("1.0", "end")

        for i, line in enumerate(text.splitlines(), start=1):
            match = pattern.match(line)
            if match:
                name = match.group(1)
                bottom_window.insert("end", f"{name}(), {i}\n")

    except:
        pass


def goto_line_selected(event=None):
    try:
        current_window = root.focus_get()

        line_text = current_window.get("insert linestart", "insert lineend")

        match = re.search(r"\d+", line_text)

        if not match:
            return

        line = int(match.group())

        if line < 1:
            return

        top_window.mark_set("insert", f"{line}.0")
        top_window.see(f"{line}.0")

        top_window.tag_add("current_line", f"{line}.0", f"{line}.0 lineend")

        top_window.focus_set()

    except:
        pass


def goto_line_num(event=None):
    try:
        line = simpledialog.askinteger("Go to line", "Enter line number:")

        if not line or line < 1:
            return

        top_window.mark_set("insert", f"{line}.0")
        top_window.see(f"{line}.0")

        top_window.tag_add("current_line", f"{line}.0", f"{line}.0 lineend")

        top_window.focus_set()

    except:
        pass


def cut_below(event=None):
    try:
        current_window = root.focus_get()

        current_window.delete("insert", "end")

    except:
        pass


def cut_above(event=None):
    try:
        current_window = root.focus_get()

        current_window.delete("1.0", "insert")

    except:
        pass


def menu_bg_color():
    try:
        color = colorchooser.askcolor()[1]
        if not color:
            return
        menubar.config(bg=color)
    except:
        pass


def menu_fg_color():
    try:
        color = colorchooser.askcolor()[1]
        if not color:
            return
        menubar.config(fg=color)
    except:
        pass


def get_colors(event=None):
    try:
        current_widget = root.focus_get()

        menu_bg = menubar.cget("bg")
        menu_fg = menubar.cget("fg")

        bg = current_widget.cget("bg")
        fg = current_widget.cget("fg")

        try:
            cursor = current_widget.cget("insertbackground")
        except:
            cursor = "default"

        output = (
            f'menu_bg = "{menu_bg}"\n'
            f'menu_fg = "{menu_fg}"\n'
            f'bg = "{bg}"\n'
            f'fg = "{fg}"\n'
            f'cursor = "{cursor}"\n'
        )

        bottom_window.delete("1.0", "end")
        bottom_window.insert("end", output)

    except:
        pass


def remove_empty_lines():
    current_widget = root.focus_get()
    text_content = current_widget.get("1.0", "end")
    non_empty_lines = [line for line in text_content.split("\n") if line.strip()]
    new_text = "\n".join(non_empty_lines)
    current_widget.delete("1.0", "end")
    current_widget.insert("1.0", new_text)


def format_python_code():
    current_widget = root.focus_get()

    try:
        input_code = current_widget.get("1.0", "end-1c")
        reformatted_code = black.format_str(input_code, mode=black.FileMode())

        current_widget.delete("1.0", "end")
        current_widget.insert("1.0", reformatted_code)

    except:
        pass


def indent_all():
    content = top_window.get("1.0", "end-1c")
    lines = content.split("\n")
    indented = "\n".join(
        "    " + line if line.strip() != "" else line for line in lines
    )
    top_window.delete("1.0", "end")
    top_window.insert("1.0", indented)


def auto_indent(event=None):
    detect_command()
    getkey = event.keysym
    current_widget = root.focus_get()
    current_line = int(current_widget.index("insert").split(".")[0])
    start_of_line = f"{current_line}.0"
    text_contents = current_widget.get(start_of_line, start_of_line + " lineend")
    indentation = text_contents[: len(text_contents) - len(text_contents.lstrip())]
    if (
        indentation
        and current_line == int(current_widget.index("insert").split(".")[0])
        and getkey == "Return"
    ):
        current_widget.insert("insert", "\n" + indentation)
        current_widget.see("insert")
        return "break"
    else:
        pass


def view_html_file():
    filename = top_window.get("insert linestart", "insert lineend").strip()

    try:
        with open(filename, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        top_window.delete("1.0", "end")
        top_window.insert("1.0", soup.prettify())

    except Exception as e:
        top_window.insert("end", f"\nError: {e}")


import html2text


def html_to_text():
    filename = top_window.get("insert linestart", "insert lineend").strip()

    try:
        with open(filename, "r", encoding="utf-8") as f:
            html = f.read()

        h = html2text.HTML2Text()
        h.ignore_images = True

        text = h.handle(html)

        top_window.delete("1.0", "end")
        top_window.insert("1.0", text)

    except Exception as e:
        top_window.insert("end", f"\nError: {e}")
        
        


def html_page_to_text():
    try:
        html = bottom_window.get("1.0", "end-1c")

        h = html2text.HTML2Text()
        h.ignore_images = True

        text = h.handle(html)

        bottom_window.delete("1.0", "end")
        bottom_window.insert("1.0", text)
        root.after(200, rewrap_text)
        

    except Exception as e:
        bottom_window.insert("end", f"\nError: {e}")


window_expanded = 0


def expand_window():
    global window_expanded

    current_widget = root.focus_get()

    if not current_widget:
        return

    try:
        window_expanded += 1

        if window_expanded > 1:
            window_expanded = 0

        if window_expanded == 1:
            current_widget.config(height=18)

        else:
            top_window.config(height=2)
            bottom_window.config(height=1)

    except:
        pass


def readonly_mode():
    widget = root.focus_get()

    try:
        widget.config(state="disabled")
    except:
        pass
        
def edit_mode():
    try:
        top_window.config(state="normal")
        bottom_window.config(state="normal")
    except:
        pass




def wiki_search():
    query = top_window.get("insert linestart", "insert lineend").strip()

    if not query:
        return

    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "exintro": True,
        "titles": query,
        "redirects": 1,
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        r = requests.get(url, params=params, headers=headers, timeout=10)

        if not r.text.strip():
            result = "Empty response"
        else:
            data = r.json()
            pages = data["query"]["pages"]
            page = next(iter(pages.values()))
            result = page.get("extract", "No summary found.")

    except Exception as e:
        result = f"Error: {e}"

    

    
    bottom_window.delete("1.0", "end")
    bottom_window.insert("end", result)
    root.after(100, html_page_to_text)
    



def rewrap_text():
    try:
        text = bottom_window.get("1.0", "end-1c")

        paragraphs = text.split("\n\n")

        result = []

        for paragraph in paragraphs:
            paragraph = " ".join(paragraph.splitlines()).strip()

            if paragraph:
                result.append(
                    textwrap.fill(paragraph, width=100)
                )

        bottom_window.delete("1.0", "end")
        bottom_window.insert("1.0", "\n\n".join(result))

    except Exception as e:
        top_window.insert("end", f"\nError: {e}")


def alphabetize():
    current_window = root.focus_get()
    try:
        lines = current_window.get("1.0", "end-1c").splitlines()

        lines = [line for line in lines if line.strip()]

        lines.sort(key=str.lower)

        current_window.delete("1.0", "end")
        current_window.insert("1.0", "\n".join(lines))

    except Exception as e:
        bottom_window.insert("end", f"\nError: {e}")



def highlight_code(event=None):
    top_window.tag_remove("kw", "1.0", "end")
    top_window.tag_remove("var", "1.0", "end")
    top_window.tag_remove("eq", "1.0", "end")
    top_window.tag_remove("num", "1.0", "end")
    top_window.tag_remove("str", "1.0", "end")
    top_window.tag_remove("call", "1.0", "end")

    text = top_window.get("1.0", "end-1c")

    for k in keyword.kwlist:
        start = "1.0"
        while True:
            pos = top_window.search(rf"\y{k}\y", start, stopindex="end", regexp=True)
            if not pos:
                break
            end = f"{pos}+{len(k)}c"
            top_window.tag_add("kw", pos, end)
            start = end

    for m in re.finditer(r"\b([A-Za-z_]\w*)\s*=", text):
        start = f"1.0+{m.start(1)}c"
        end = f"1.0+{m.end(1)}c"
        top_window.tag_add("var", start, end)

    for m in re.finditer(r"=", text):
        p = f"1.0+{m.start()}c"
        top_window.tag_add("eq", p, f"{p}+1c")

    for m in re.finditer(r"\b\d+(\.\d+)?\b", text):
        start = f"1.0+{m.start()}c"
        end = f"1.0+{m.end()}c"
        top_window.tag_add("num", start, end)

    for m in re.finditer(r'".*?"|\'.*?\'', text):
        start = f"1.0+{m.start()}c"
        end = f"1.0+{m.end()}c"
        top_window.tag_add("str", start, end)

    for m in re.finditer(r"\b([A-Za-z_]\w*)\(", text):
        start = f"1.0+{m.start(1)}c"
        end = f"1.0+{m.end(1)}c"
        top_window.tag_add("call", start, end)

    top_window.tag_config("kw", foreground="yellow")
    top_window.tag_config("var", foreground="cyan")
    top_window.tag_config("eq", foreground="gold")
    top_window.tag_config("num", foreground="light grey")
    top_window.tag_config("str", foreground="orange")
    top_window.tag_config("call", foreground="magenta")
    



root = tk.Tk()
root.title("Dev Editor")
root.geometry("470x750")

root.config(bg="beige")

top_window = scrolledtext.ScrolledText(
    root,
    wrap="word",
    font=("Courier New", 7),
    bg="black",
    fg="white",

    undo=True,
    height=2,
    padx=9,
    pady=9,
    insertbackground="orange",
    insertwidth=4,
    bd=5,
)

top_window.pack(
    expand=True,
    fill=tk.BOTH,
    side=tk.TOP
)

bottom_window = scrolledtext.ScrolledText(
    root,
    wrap="word",
    font=("Courier New", 7),
    bg="#001000",
    fg="lightgreen",
    height=1,
    padx=8,
    pady=9,
    bd=10,
    insertbackground="yellow",
    insertwidth=4,
)

bottom_window.pack(
    expand=True,
    fill=tk.BOTH
)

top_window.tag_config("kw", foreground="gold")


menubar = tk.Menu(
    root,
    bd=5,
    font=("Times", 9),
)


file_menu = tk.Menu(
    menubar,
    tearoff=0,
    bg="white",
    font=("Courier New", 9),
)

menubar.add_cascade(label="File", menu=file_menu)


file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)

file_menu.add_command(label="[Expand]", command=expand_window)


file_menu.add_command(label="View File At Cursor", command=open_file_from_cursor)

file_menu.add_command(label="View Raw HTML File", command=view_html_file)

file_menu.add_command(label="HTML → Text", command=html_to_text)

file_menu.add_command(label="Save", command=save_file)

file_menu.add_command(label="Read-Only", command=readonly_mode)

file_menu.add_command(label="Edit Mode", command=edit_mode)

file_menu.add_command(label="Search Text", command=search_word)

file_menu.add_command(label="Web Browser", command=web_browser)

file_menu.add_command(label="Wiki Search", command=wiki_search)


file_menu.add_command(label="Font Size", command=set_font_size)

file_menu.add_command(label="Go To Line", command=goto_line_num)

file_menu.add_separator()


file_menu.add_command(label="Quit", command=root.destroy)


edit_menu = tk.Menu(
    menubar,
    tearoff=0,
    bg="yellow",
    font=("Courier New", 9),
)
edit_menu.add_command(label="Undo ←", command=lambda: top_window.edit_undo())
edit_menu.add_command(label="Redo →", command=lambda: top_window.edit_redo())

edit_menu.add_command(label="Remove Empty Lines", command=remove_empty_lines)



edit_menu.add_command(label="Indent All →", command=indent_all)

edit_menu.add_command(label="Select All", command=select_all_text)

edit_menu.add_command(label="Cut Text", command=cut_text)

edit_menu.add_command(label="Copy Text", command=copy_text)

edit_menu.add_command(label="Paste Text", command=paste_text)


edit_menu.add_command(label="Cut Above↑", command=cut_above)

edit_menu.add_command(label="Cut Below↓", command=cut_below)


menubar.add_cascade(label="Edit", menu=edit_menu)

color_menu = tk.Menu(
    menubar,
    tearoff=0,
    bg="lightgreen",
    fg="#003300",
    font=("Courier New", 9),
)

menubar.add_cascade(label="Color", menu=color_menu)

color_menu.add_command(label="Menu Background", command=menu_bg_color)

color_menu.add_command(label="Menu Foreground", command=menu_fg_color)

color_menu.add_command(label="Background Color", command=set_bg)
color_menu.add_command(label="Foreground Color", command=set_fg)
color_menu.add_command(label="Cursor Color", command=set_cursor)


color_menu.add_command(label="Get Colors", command=get_colors)


format_menu = tk.Menu(
    menubar,
    tearoff=0,
    bg="lightcyan",
    fg="darkblue",
    font=("Courier New", 9),
)

menubar.add_cascade(label="Format", menu=format_menu)

format_menu.add_command(label="Format Python", command=format_python_code)

format_menu.add_command(label="Format HTML Page", command=html_page_to_text)

format_menu.add_command(label="Alphabetize (AZ↓)", command=alphabetize)

format_menu.add_command(label="Format Flake 8", command=format_flake8)


format_menu.add_command(label="Format Cpplint", command=format_cpplint)


dev_menu = tk.Menu(menubar, tearoff=0, font=("Courier New", 9), bg="gold", fg="#000044")

menubar.add_cascade(label="Dev", menu=dev_menu)

dev_menu.add_command(label="Unix Command", command=run_command)

dev_menu.add_command(label="Run Python", command=run_python)

dev_menu.add_command(label="Compile & Run C", command=compile_run_c)
dev_menu.add_command(label="Compile & Run C++", command=compile_run_cpp)

dev_menu.add_command(label="Compile C++", command=compile_cpp)

dev_menu.add_command(label="Run Compiled C++", command=exe_cpp)

dev_menu.add_command(label="Run Flake 8", command=run_flake8)


dev_menu.add_command(label="Run Cpplint", command=run_cpplint)



dev_menu.add_command(label="Highlight Code", command=highlight_code)

dev_menu.add_command(label="Remove Highlights", command=remove_highlights)

dev_menu.add_command(label="List Functions", command=list_functions)


root.config(menu=menubar)


def on_closing():
    with open("last_code.txt", "w") as f:
        f.write(top_window.get(1.0, "end-1c"))


root.protocol("WM_DELETE_WINDOW", on_closing)

try:
    with open("last_code.txt", "r") as f:
        top_window.insert(1.0, f.read())

except:
    pass


top_window.focus_set()

top_window.bind("<Return>", auto_indent)

bottom_window.bind("<Button-1>", goto_line_selected)


root.mainloop()

