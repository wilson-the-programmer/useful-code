
import tempfile
import random
import io
import os
import sys
import subprocess
import threading
import webbrowser
import urllib.parse
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

import keyword
import re

from xml.etree import ElementTree


import black
import requests

from bs4 import BeautifulSoup

from jnius import autoclass


from pypinyin import pinyin, Style
from deep_translator import GoogleTranslator


from transliterate import translit


c_keywords = ["auto","break","case","char","const","continue","default","do","double","else","enum","extern","float","for","goto","if","inline","int","long","register","restrict","return","short","signed","sizeof","static","struct","switch","typedef","union","unsigned","void","volatile","while"]

unix_words = ["ls", "cat", "cp", "mv", "rm", "mkdir", "rmdir", "pwd", "cd", "echo", "touch", "clear", "whoami", "date", "cal", "grep", "find", "sort", "wc", "head", "tail", "less", "more", "gcc", "g++", "python", "python3", "flake8", "cpplint", "git", "make", "cmake", "ps", "top", "kill", "chmod", "chown"]





def search_from_cursor():
    widget = root.focus_get()
    if widget is None:
        return

    try:
        text = widget.get("insert linestart", "insert lineend").strip()

        if not text:
            return

        if text.lower().endswith((".com", ".org", ".net", ".edu", ".gov", ".io")):
            webbrowser.open_new_tab("https://" + text)
        else:
            query = urllib.parse.quote_plus(text)
            webbrowser.open_new_tab(
                f"https://www.bing.com/search?q={query}"
            )

    except:
        pass


def search_selected():
    try:
        widget = root.focus_get()
        text = widget.selection_get().strip()

        if not text:
            return

        if text.lower().endswith((".com", ".org", ".net", ".edu", ".gov", ".io")):
            webbrowser.open_new_tab("https://" + text)
        else:
            query = urllib.parse.quote_plus(text)
            webbrowser.open_new_tab(
                f"https://www.bing.com/search?q={query}"
            )

    except:
        pass
        

def undo_last():
    try:
        editor.edit_undo()
    except:
        pass


def redo_last():
    try:
        editor.edit_redo()
    except:
        pass


def list_files():
    current_window = root.focus_get()
    last_location = current_window.index("insert")
    line_content = current_window.get("insert linestart", "insert lineend")
    letter = line_content.strip().lower()
    process = subprocess.Popen(
        ["ls"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
    )
    output, _ = process.communicate()
    command_list = output.decode().splitlines()
    filtered_commands = [cmd for cmd in command_list if cmd.lower().startswith(letter)]
    if filtered_commands:
        current_window.delete("insert lineend", "end")
        for cmd in filtered_commands:
            current_window.insert("end", f"\n{cmd}")
    current_window.mark_set("insert", last_location)
    current_window.see("insert")


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


def auto_indent(event=None):
    detect_command()
    show_whitespaces()
    current_widget = root.focus_get()
    current_line = int(current_widget.index("insert").split(".")[0])
    start_of_line = f"{current_line}.0"
    text_contents = current_widget.get(start_of_line, start_of_line + " lineend")
    indentation = text_contents[: len(text_contents) - len(text_contents.lstrip())]
    if (
        indentation
        and current_line == int(current_widget.index("insert").split(".")[0])
    ):
        current_widget.insert("insert", "\n" + indentation)
        current_widget.see("insert")
        return "break"
    else:
        pass


def highlight_code(event=None):
    editor.tag_remove("kw", "1.0", "end")
    editor.tag_remove("var", "1.0", "end")
    editor.tag_remove("eq", "1.0", "end")
    editor.tag_remove("num", "1.0", "end")
    editor.tag_remove("str", "1.0", "end")
    editor.tag_remove("call", "1.0", "end")

    text = editor.get("1.0", "end-1c")

    for k in keyword.kwlist + c_keywords:
        start = "1.0"
        while True:
            pos = editor.search(rf"\y{k}\y", start, stopindex="end", regexp=True)
            if not pos:
                break
            end = f"{pos}+{len(k)}c"
            editor.tag_add("kw", pos, end)
            start = end

    for m in re.finditer(r"\b([A-Za-z_]\w*)\s*=", text):
        start = f"1.0+{m.start(1)}c"
        end = f"1.0+{m.end(1)}c"
        editor.tag_add("var", start, end)

    for m in re.finditer(r"=", text):
        p = f"1.0+{m.start()}c"
        editor.tag_add("eq", p, f"{p}+1c")

    for m in re.finditer(r"\b\d+(\.\d+)?\b", text):
        start = f"1.0+{m.start()}c"
        end = f"1.0+{m.end()}c"
        editor.tag_add("num", start, end)

    for m in re.finditer(r'".*?"|\'.*?\'', text):
        start = f"1.0+{m.start()}c"
        end = f"1.0+{m.end()}c"
        editor.tag_add("str", start, end)

    for m in re.finditer(r"\b([A-Za-z_]\w*)\(", text):
        start = f"1.0+{m.start(1)}c"
        end = f"1.0+{m.end(1)}c"
        editor.tag_add("call", start, end)

    editor.tag_config("kw", foreground="red")
    editor.tag_config("var", foreground="#8B5A2B")
    editor.tag_config("eq", foreground="#333333")
    editor.tag_config("num", foreground="blue")
    editor.tag_config("str", foreground="#E67300")
    editor.tag_config("call", foreground="green")

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

        editor.mark_set("insert", f"{line}.0")
        editor.see(f"{line}.0")

        editor.tag_add("current_line", f"{line}.0", f"{line}.0 lineend")
        

        editor.focus_set()
        highlight_line()

    except:
        pass

def show_output(result):
    output_window = tk.Toplevel(root)
    output_window.geometry("460x500+0+0")
    

    result_text = tk.Text(
        output_window,
        wrap="word",
        font=("Courier New", 8),
        height=5,
        bg="white",
        fg="black",
        padx=8,
        pady=8,
        bd=2,
        insertbackground="red",
        insertwidth=6
    )
    result_text.pack(
        fill="both",
        expand=True
    )

    result_text.insert("1.0", result)
        
    exit_button = tk.Button(
        output_window,
        text="Exit",
        command=lambda: output_window.destroy(),
        font=("Courier New", 8),
        bd=5,
        width=2,
        bg="lightgrey",
        fg="darkblue" 
            
    )
        
    exit_button.pack(side="left")
    
    format_button = tk.Button(
        output_window,
        text="Format",
        command=lambda: (root.geometry("460x300"), output_window.geometry("460x230+0+330"), format_flake8()),
        font=("Courier New", 8),
        bd=5,
        width=2,
        bg="lightgreen",
        fg="#004400" 
            
    )
        
    format_button.pack(side="left")
    result_text.focus_set()
    	
    output_window.bind("<Button-1>", goto_line_selected)


def run_python():
    current_widget = root.focus_get()
    code = current_widget.get("1.0", tk.END)

    output = io.StringIO()
    sys.stdout = output

    try:
        exec(code)

    except Exception as e:
        output.write(f"{type(e).__name__}: {e}")

    finally:
        sys.stdout = sys.__stdout__

        show_output(output.getvalue())
        



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


def save_file():
    current_window = root.focus_get()
    filename = filedialog.asksaveasfilename(
        defaultextension=".txt"
    )

    if filename:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(current_window.get("1.0", "end-1c"))
            

def clear_editor():
	editor.delete(1.0, "end")

def eval_exp():
    exp = editor.get("insert linestart", "insert lineend").strip()
    try:
        result = eval(exp)

        if isinstance(result, float):
            result = round(result, 3)

        editor.insert("insert", f" ≈ {result}")
        editor.event_generate("<Return>")
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
        


def detect_command(event=None):
    current_window = root.focus_get()
    cmd = current_window.get("insert linestart", "insert lineend").strip()
    for c in unix_words:
        if c in cmd:
            unix_command()
            current_window.event_generate("return")


def unix_command():
    current_window = root.focus_get()
    command = current_window.get("insert linestart", "insert lineend").strip()

    def run_command():
        try:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                text=True
            )

            for line in process.stdout:
                current_window.insert("end", line)
                current_window.see("end")

            process.stdout.close()
            process.wait()

        except:
            pass

        current_window.see("end")

    current_window.see("insert")
    threading.Thread(target=run_command).start()


window_expanded = 0


def expand_window():
    global window_expanded

    try:
        window_expanded += 1

        if window_expanded > 1:
            window_expanded = 0

        if window_expanded == 1:
            editor.config(height=10)
            root.geometry("460x750+0+0")
        else:
            root.geometry("460x440+0+0")
            editor.config(height=5)

    except:
        pass


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
        link_frame.pack(
            padx=5,
            pady=10,
            fill=tk.BOTH,
            expand=False
        )
        
        webpage_viewer.pack_forget()
        
        webpage_viewer.pack(
            padx=0,
            pady=0,
            fill=tk.BOTH,
            expand=True,
            side=tk.BOTTOM,
            ipadx=0,
            ipady=0
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
        #webpage_viewer.config(state=tk.NORMAL)
        webpage_viewer.delete("1.0", tk.END)
        webpage_viewer.insert(tk.END, content)
        #webpage_viewer.config(state=tk.DISABLED)

    def clear_links():
        for widget in link_frame.winfo_children():
            widget.destroy()
        link_frame.pack_forget()
        webpage_viewer.pack_forget()
        webpage_viewer.pack(padx=0, pady=0, fill=tk.BOTH, expand=True, side=tk.BOTTOM)
    """
    do not delete this function below because the links buttons depend on this.
    """
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
            lambda: threading.Thread(target=fetch_suggestions,
            daemon=True).start()
        )



    browser_root = tk.Toplevel(root)
    browser_root.title("Web Browser")
    browser_root.geometry("460x750+0+0")
    browser_root.config(bg="white")

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
        text="Cls",
        width=1,
        bg="#550000",
        fg="red",
        command=lambda: entry.delete(1.0, "end"),
        font=("Times", 9),
        relief="raised",
        bd=2,
    )
    clear_button.pack(side=tk.LEFT)
    
    url_button = tk.Button(
        button_frame,
        text="Link",
        width=1,
        bg="gold",
        command=lambda: (entry.delete(1.0, "end"), paste_last_link()),
        font=("Times", 9),
        relief="raised",
        bd=4,
    )
    url_button.pack(side=tk.LEFT)
    
    copy_button = tk.Button(
        button_frame,
        text="Copy",
        width=1,
        bg="lightcyan",
        command=copy_text,
        font=("Courier New", 9),
        relief="raised",
        bd=4,
    )
    copy_button.pack(side=tk.LEFT)
    
    paste_button = tk.Button(
        button_frame,
        text="Paste",
        width=1,
        bg="lightgreen",
        command=paste_text,
        font=("Courier New", 9),
        relief="raised",
        bd=4,
    )
    paste_button.pack(side=tk.LEFT)
    
    
    
    expand_button = tk.Button(
        button_frame,
        text="[]",
        width=1,
        bg="gold",
        command=clear_links,
        font=("Times", 9),
        relief="raised",
        bd=4,
    )
    expand_button.pack(side=tk.LEFT)
    search_button = tk.Button(
        button_frame,
        text="Search",
        width=2,
        bg="white",
        fg="blue",
        command=search_and_display_links,
        font=("Times", 9, "bold"),
        relief="raised",
        bd=4,
    )
    search_button.pack(side=tk.LEFT)
    
    link_frame = tk.Frame(browser_root)
    
    link_frame.pack(
        padx=5,
        pady=10,
        fill=tk.BOTH,
        expand=False
    )
    
    webpage_viewer = scrolledtext.ScrolledText(
        browser_root,
        width=40,
        height=9,
        wrap=tk.WORD,
        bg="white",
        fg="darkblue",
        font=("Noto Sans Mono CJK JP", 9),
        padx=10,
        pady=10,
        bd=5,
        insertbackground="darkred",
        insertwidth=5,
    )
    webpage_viewer.pack(
        padx=0,
        pady=0,
        fill=tk.BOTH,
        expand=True,
        side=tk.BOTTOM
    )

    entry.bind("<KeyRelease>", schedule_fetch)
    
    menubar = tk.Menu(
        root,
        bd=5,
        font=("Courier New", 11)
    )

    browser_root.config(menu=menubar)


    file_menu = tk.Menu(
        menubar,
        tearoff=0,
        bg="white",
        font=("Courier New", 11),
    )

    menubar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Open File", command=open_file)
    file_menu.add_command(label="Save", command=save_file)
    file_menu.add_command(label="Edit Mode", command=lambda: webpage_viewer.config(state=tk.NORMAL))
    file_menu.add_command(label="Read Only", command=lambda: webpage_viewer.config(state=tk.DISABLED))
    
    file_menu.add_command(label="Select All & Copy", command=select_all_copy)
    
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=lambda: browser_root.destroy())
    
    
    web_menu = tk.Menu(
        menubar,
        tearoff=0,
        bg="white",
        font=("Courier New", 11),
    )

    menubar.add_cascade(label="Web", menu=web_menu)
    web_menu.add_command(label="Chrome Selected Text", command=search_selected)
    web_menu.add_command(label="Search From Cursor", command=search_from_cursor)
    
    
    
    
    
    
    browser_root.mainloop()









def show_whitespaces(event=None):
    editor.tag_remove("trail_ws", "1.0", "end")

    text = editor.get("1.0", "end-1c")
    lines = text.splitlines()

    for i, line in enumerate(lines, start=1):
        match = re.search(r"(?<=\S)[ \t]+$", line)
        if match:
            start = f"{i}.{match.start()}"
            end = f"{i}.{match.end()}"
            editor.tag_add("trail_ws", start, end)

    editor.tag_config("trail_ws", background="red")


def remove_whitespaces():
    w = root.focus_get()

    try:
        text = w.get("1.0", "end-1c")
        lines = text.splitlines()

        cleaned = [line.rstrip(" \t") for line in lines]

        w.delete("1.0", "end")
        w.insert("1.0", "\n".join(cleaned))

    except:
        pass


def highlight_line():
    w = root.focus_get()

    try:
        line_start = w.index("insert linestart")
        line_end = w.index("insert lineend")

        tag = "cursor_line"

        w.tag_add(tag, line_start, line_end)
        w.tag_config(tag, background="lightgreen", foreground="#003300")

    except:
        pass


def select_all_copy():
    widget = root.focus_get()

    if widget is None:
        return

    try:
        widget.tag_add("sel", "1.0", "end")
        widget.clipboard_clear()
        widget.clipboard_append(widget.get("1.0", "end-1c"))
        return
    except:
        pass

    try:
        widget.select_range(0, "end")
        widget.clipboard_clear()
        widget.clipboard_append(widget.get())
    except:
        pass
        
def edit_mode():
    current_window = root.focus_get()
    if current_window is None:
        return

    try:
        current_window.config(state=tk.NORMAL)
    except:
        pass


   
def read_only():
    current_window = root.focus_get()
    if current_window is None:
        return

    try:
        current_window.config(state=tk.DISABLED)
    except:
        pass


               
def mandarin_translator():
    current_window = root.focus_get()
    text = current_window.get("insert linestart", "insert lineend").strip()

    if not text:
        return

    try:
        chinese = GoogleTranslator(source="auto", target="zh-CN").translate(text)

        pinyin_text = " ".join(item[0] for item in pinyin(chinese, style=Style.TONE))
        

        current_window.insert("insert", f"\n\n{chinese}\n" f"{pinyin_text}\n\n")
        current_window.see("insert")

    except:
        pass
                     
def compile_exe_c():
    def task():
        try:
            code = editor.get("1.0", "end-1c")

            f = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".c",
                mode="w",
                encoding="utf-8"
            )

            f.write(code)
            f.close()

            exe = f.name + ".out"

            try:
                c = subprocess.run(["gcc", f.name, "-o", exe], capture_output=True, text=True)

                if c.returncode != 0:
                    show_output(c.stderr)
                    return

                r = subprocess.run([exe], capture_output=True, text=True)

                show_output(r.stdout + r.stderr)

            finally:
                if os.path.exists(f.name):
                    os.unlink(f.name)

                if os.path.exists(exe):
                    os.unlink(exe)

        except Exception as e:
            show_output(str(e))

    threading.Thread(target=task, daemon=True).start()            

              
def goto_line_num(event=None):
    try:
        line = simpledialog.askinteger("Go to line", "Enter line number:")

        if not line or line < 1:
            return

        editor.mark_set("insert", f"{line}.0")
        editor.see(f"{line}.0")

        editor.tag_add("current_line", f"{line}.0", f"{line}.0 lineend")

        editor.focus_set()

    except:
        pass


def go_to_top():
    widget = root.focus_get()
    if widget is None:
        return
    try:
        widget.mark_set("insert", "1.0")
        widget.see("1.0")
    except:
        pass


def go_to_bottom():
    widget = root.focus_get()
    if widget is None:
        return
    try:
        widget.mark_set("insert", "end")
        widget.see("end")
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



def bg_color():
    try:
        color = colorchooser.askcolor()[1]
        if not color:
            return
        editor.config(bg=color)
    except:
        pass


def fg_color():
    try:
        color = colorchooser.askcolor()[1]
        if not color:
            return
        editor.config(fg=color)
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


        editor.insert(1.0, f"{output}\n")

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
    content = editor.get("1.0", "end-1c")
    lines = content.split("\n")
    indented = "\n".join(
        "    " + line if line.strip() != "" else line for line in lines
    )
    editor.delete("1.0", "end")
    editor.insert("1.0", indented)


def run_flake8():
    def task():
        try:
            code = editor.get("1.0", "end-1c")

            f = tempfile.NamedTemporaryFile(
                delete=False, suffix=".py", mode="w", encoding="utf-8"
            )
            f.write(code)
            f.close()

            result = subprocess.run(["flake8", f.name], capture_output=True, text=True)


            if result.stdout.strip():
                show_output(result.stdout)
                #root.after(100, format_flake8)
            elif result.stderr.strip():
                show_output(result.stderr)
            else:
                show_output("No issues found")

            os.unlink(f.name)

        except:
            pass

    threading.Thread(target=task, daemon=True).start()


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

            line_number = int(m.group(2))

            message = m.group(5).strip()

            if message:
                message = message[0].upper() + message[1:]

            if not message.endswith("."):
                message += "."

            grouped.setdefault(line_number, []).append(message)

        output = []

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






        

root = tk.Tk()
root.title("Python IDE")
root.config(bg="white")
root.geometry("460x440+0+0")
editor = tk.Text(
    root,
    wrap="word",
    font=("Courier New", 8),
    undo=True,
    height=5,
    bd=5,
    padx=8,
    pady=8,
    bg="white",
    fg="black",
    insertwidth=6,
    insertbackground="darkred"
)
editor.pack(
    expand=True,
    fill="both",
    side="top"
)



menubar = tk.Menu(
    root,
    bd=5,
    font=("Courier New", 10),
)

root.config(menu=menubar)


file_menu = tk.Menu(
    menubar,
    tearoff=0,
    bg="white",
    font=("Courier New", 10),
)

menubar.add_cascade(label="File", menu=file_menu)


file_menu.add_command(label="New (Blank Page)", command=clear_editor)

file_menu.add_command(label="Open File", command=open_file)
file_menu.add_command(label="Save", command=save_file)


file_menu.add_command(label="Line Number", command=goto_line_num)

file_menu.add_command(label="Top↑", command=go_to_top)

file_menu.add_command(label="Botto.↓", command=go_to_bottom)




file_menu.add_command(label="Read Only", command=read_only)

file_menu.add_command(label="Edit Mode", command=edit_mode)

file_menu.add_command(label="Web Browser", command=web_browser)

file_menu.add_command(label="中国人 Mandarin", command=mandarin_translator)

file_menu.add_command(label="Exit", command=lambda: root.destroy())


edit_menu = tk.Menu(
    menubar,
    tearoff=0,
    bg="white",
    font=("Courier New", 10),
)

menubar.add_cascade(label="Edit", menu=edit_menu)


edit_menu.add_command(label="Undo", command=undo_last)

edit_menu.add_command(label="Re-do", command=redo_last)


edit_menu.add_command(label="Cut", command=cut_text)

edit_menu.add_command(label="Copy", command=copy_text)

edit_menu.add_command(label="Paste", command=paste_text)

edit_menu.add_command(label="Cut Above↑", command=cut_above)

edit_menu.add_command(label="Cut Below↓", command=cut_below)


edit_menu.add_command(label="Select All & Copy", command=select_all_copy)

edit_menu.add_command(label="Remove Empty Lines", command=remove_empty_lines)

edit_menu.add_command(label="Indent All →", command=indent_all)

dev_menu = tk.Menu(
    menubar,
    tearoff=0,
    bg="white",
    font=("Courier New", 10),
)

menubar.add_cascade(label="Dev", menu=dev_menu)


dev_menu.add_command(label="C >", command=compile_exe_c)


dev_menu.add_command(label="Unix Command >", command=unix_command)

dev_menu.add_command(label="Python >", command=run_python)

dev_menu.add_command(label="Run Flake8", command=run_flake8)


dev_menu.add_command(label="Highlight Code", command=highlight_code)

dev_menu.add_command(label="Show Trailing Spaces", command=show_whitespaces)

dev_menu.add_command(label="Format Python", command=format_python_code)




dev_menu.add_command(label="Remove Trailing Spaces", command=remove_whitespaces)


colors_menu = tk.Menu(
    menubar,
    tearoff=0,
    bg="white",
    font=("Courier New", 10),
)

menubar.add_cascade(label="Col", menu=colors_menu)


colors_menu.add_command(label="Menu Back", command=menu_bg_color)

colors_menu.add_command(label="Menu Fore", command=menu_fg_color)

colors_menu.add_command(label="Editor Back", command=bg_color)

colors_menu.add_command(label="Editor Fore", command=fg_color)

colors_menu.add_command(label="Get Colors", command=get_colors)



files_button = tk.Button(
    root,
    text="ls *",
    font=("Times", 8, "bold"),
    bg="black",
    fg="lightgreen",
    width=1,
    bd=6,
    command=list_files
)
files_button.pack(side="left")

view_button = tk.Button(
    root,
    text="View",
    font=("Times", 8, "bold"),
    bg="black",
    fg="lightgrey",
    width=1,
    bd=6,
    command=open_file_from_cursor
)
view_button.pack(side="left")

clear_button = tk.Button(
    root,
    text="中国人",
    font=("Times", 8, "bold"),
    bg="white",
    fg="green",
    width=1,
    bd=6,
    command=mandarin_translator
)
clear_button.pack(side="left")


undo_button = tk.Button(
    root,
    text="P >",
    font=("Times", 8, "bold"),
    bg="lightcyan",
    fg="darkblue",
    width=1,
    bd=6,
    command=run_python
)
undo_button.pack(side="left")

web_button = tk.Button(
    root,
    text="Web",
    font=("Times", 8, "bold"),
    bg="blue",
    fg="lightcyan",
    width=1,
    bd=6,
    command=web_browser
)
web_button.pack(side="left")


expand_button = tk.Button(
    root,
    text="[]",
    font=("Times", 8, "bold"),
    bg="black",
    fg="orange",
    width=1,
    bd=6,
    command=expand_window
)
expand_button.pack(side="left")

# Reload whatever was in editor
def on_closing():
    with open("last_code.txt", "w") as f:
        f.write(editor.get(1.0, "end-1c"))


root.protocol("WM_DELETE_WINDOW", on_closing)

try:
    with open("last_code.txt", "r") as f:
        editor.insert(1.0, f.read())

except:
    pass


editor.focus_set()


editor.bind("<Return>", auto_indent)

root.mainloop()


