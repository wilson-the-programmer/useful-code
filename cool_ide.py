from flask import Flask, request
import subprocess
import tempfile
import os
import io
import sys

app = Flask(__name__)

saved_html = "<h1>No HTML loaded</h1>"

@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">

<style>
body {
    margin: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    font-family: Arial;
    background: gold;
    padding-top: 14px;
}

.window {
    width: 95%;
    height: 245px;
    font-size: 18px;
    font-family: "Courier New";
    font-weight: bold;
    border: 3px solid black;
    border-radius: 4px;
    padding: 6px;
    margin-bottom: 15px;
    background: #ffffff;
    color: #000000;
    box-sizing: border-box;
    overflow-y: auto;
}

#editor {
    white-space: pre-wrap;
    outline: none;
}

#output {
    white-space: pre-wrap;
    overflow-y: auto;
}

#buttonRow {
    width: 95%;
    display: flex;
    gap: 4px;
    margin-bottom: 15px;
}

.btn {
    flex: 1;
    height: 50px;
    font-size: 20px;
    font-family: "Courier New";
    font-weight: bold;
    border: 2px solid black;
    border-radius: 12px;
    background: lightyellow;
    color: black;
    cursor: pointer;
}

.btn:active {
    transform: scale(0.96);
    background: #111827;
}
</style>

<script>

function getCode() {
    return document.getElementById("editor").innerText;
}

function insertAtCursor(text) {
    const el = document.getElementById("editor");
    el.focus();

    const sel = window.getSelection();
    const range = sel.getRangeAt(0);

    range.deleteContents();
    range.insertNode(document.createTextNode(text));
    range.collapse(false);

    sel.removeAllRanges();
    sel.addRange(range);
}

function runHTML() {
    const code = getCode();

    fetch("/set_html", {
        method: "POST",
        headers: {"Content-Type": "application/x-www-form-urlencoded"},
        body: "html=" + encodeURIComponent(code)
    }).then(() => {
        window.open("/view_html", "_blank");
    });
}

function runPython() {
    const code = getCode();

    fetch("/run_python", {
        method: "POST",
        headers: {"Content-Type": "application/x-www-form-urlencoded"},
        body: "code=" + encodeURIComponent(code)
    })
    .then(r => r.text())
    .then(data => {
        document.getElementById("output").innerText = data;
    });
}

function runRust() {
    const code = getCode();

    fetch("/run_rust", {
        method: "POST",
        headers: {"Content-Type": "application/x-www-form-urlencoded"},
        body: "code=" + encodeURIComponent(code)
    })
    .then(r => r.text())
    .then(data => {
        document.getElementById("output").innerText = data;
    });
}

function runGo() {
    const code = getCode();

    fetch("/run_go", {
        method: "POST",
        headers: {"Content-Type": "application/x-www-form-urlencoded"},
        body: "code=" + encodeURIComponent(code)
    })
    .then(r => r.text())
    .then(data => {
        document.getElementById("output").innerText = data;
    });
}

function runUnix() {
    const cmd = window.getSelection().toString().trim() || getCode().trim().split("\\n").pop().trim();

    fetch("/run_unix", {
        method: "POST",
        headers: {"Content-Type": "application/x-www-form-urlencoded"},
        body: "cmd=" + encodeURIComponent(cmd)
    })
    .then(r => r.text())
    .then(data => {
        insertAtCursor("\\n" + data + "\\n");
    });
}

</script>

</head>

<body>

<div id="editor" class="window" contenteditable="true"></div>

<div id="buttonRow">
    <button class="btn" onclick="runUnix()">Unix</button>
    <button class="btn" onclick="runHTML()">HTML</button>
    <button class="btn" onclick="runPython()">P ></button>
    <button class="btn" onclick="runRust()">Rust</button>
    <button class="btn" onclick="runGo()">Go ></button>
</div>

<div id="output" class="window"></div>

</body>
</html>
"""

@app.route("/set_html", methods=["POST"])
def set_html():
    global saved_html
    saved_html = request.form.get("html", "")
    return "ok"

@app.route("/view_html")
def view_html():
    return saved_html

@app.route("/run_python", methods=["POST"])
def run_python():
    code = request.form.get("code", "")
    buffer = io.StringIO()
    sys.stdout = buffer
    try:
        exec(code)
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
    finally:
        sys.stdout = sys.__stdout__
    return buffer.getvalue()

@app.route("/run_rust", methods=["POST"])
def run_rust():
    code = request.form.get("code", "")
    tmp = None
    exe = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".rs") as f:
            f.write(code.encode())
            tmp = f.name

        exe = tmp.replace(".rs", "")

        subprocess.check_output(["rustc", tmp, "-o", exe], stderr=subprocess.STDOUT)
        result = subprocess.check_output([exe], stderr=subprocess.STDOUT).decode()
        return result
    except subprocess.CalledProcessError as e:
        return e.output.decode()
    finally:
        for p in [tmp, exe]:
            if p and os.path.exists(p):
                os.remove(p)

@app.route("/run_go", methods=["POST"])
def run_go():
    code = request.form.get("code", "")
    tmp = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".go") as f:
            f.write(code.encode())
            tmp = f.name

        result = subprocess.check_output(
            ["go", "run", tmp],
            stderr=subprocess.STDOUT
        ).decode()

        return result
    except subprocess.CalledProcessError as e:
        return e.output.decode()
    finally:
        if tmp and os.path.exists(tmp):
            os.remove(tmp)

@app.route("/run_unix", methods=["POST"])
def run_unix():
    cmd = request.form.get("cmd", "")
    if not cmd.strip():
        return ""
    try:
        result = subprocess.check_output(
            cmd,
            shell=True,
            stderr=subprocess.STDOUT,
            executable="/bin/bash"
        ).decode()
        return result
    except subprocess.CalledProcessError as e:
        return e.output.decode()

if __name__ == "__main__":
    app.run(port=8700)
