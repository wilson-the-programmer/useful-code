def highlight_code(event=None):
    current_window = root.focus_get()

    line = int(current_window.index("insert").split(".")[0])

    first = max(1, line - 20)
    last = line + 20

    region_start = f"{first}.0"
    region_end = f"{last}.end"

    for tag in ("kw", "var", "eq", "num", "str", "call"):
        current_window.tag_remove(tag, region_start, region_end)

    text = current_window.get(region_start, region_end)

    for k in keyword.kwlist:
        for m in re.finditer(rf"\b{re.escape(k)}\b", text):
            s = current_window.index(f"{region_start}+{m.start()}c")
            e = current_window.index(f"{region_start}+{m.end()}c")
            current_window.tag_add("kw", s, e)

    for m in re.finditer(r"\b([A-Za-z_]\w*)\s*=", text):
        s = current_window.index(f"{region_start}+{m.start(1)}c")
        e = current_window.index(f"{region_start}+{m.end(1)}c")
        current_window.tag_add("var", s, e)

    for m in re.finditer(r"=", text):
        s = current_window.index(f"{region_start}+{m.start()}c")
        current_window.tag_add("eq", s, f"{s}+1c")

    for m in re.finditer(r"\b\d+(\.\d+)?\b", text):
        s = current_window.index(f"{region_start}+{m.start()}c")
        e = current_window.index(f"{region_start}+{m.end()}c")
        current_window.tag_add("num", s, e)

    for m in re.finditer(r'"[^"\n]*"|\'[^\'\n]*\'', text):
        s = current_window.index(f"{region_start}+{m.start()}c")
        e = current_window.index(f"{region_start}+{m.end()}c")
        current_window.tag_add("str", s, e)

    for m in re.finditer(r"\b([A-Za-z_]\w*)\(", text):
        s = current_window.index(f"{region_start}+{m.start(1)}c")
        e = current_window.index(f"{region_start}+{m.end(1)}c")
        current_window.tag_add("call", s, e)

    current_window.tag_config("kw", foreground="red")
    current_window.tag_config("var", foreground="#000042")
    current_window.tag_config("eq", foreground="#222222")
    current_window.tag_config("num", foreground="red")
    current_window.tag_config("str", foreground=quick_hex(140,0,0))
    current_window.tag_config("call", foreground="darkblue")

