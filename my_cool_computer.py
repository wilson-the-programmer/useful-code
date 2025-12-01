from flask import Flask, request, render_template_string
import subprocess
import tempfile
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>My Computer</title>
<meta charset="UTF-8">
<style>
body {
    background: #1e1e1e;
    color: #e5e5e5;
    font-family: monospace;
    margin: 0;
    padding: 0;
    display: flex;
    justify-content: center;
}
.container {
    width: 80%;
    max-width: 900px;
    padding: 20px;
}
textarea {
    width: 100%;
    height: 380px;
    background: #111;
    color: white;
    font-weight: bold;
    text-shadow: 0 0 3px white;
    border: 1px solid #777;
    padding: 14px;
    font-size: 40px;
    overflow-y: scroll;
    resize: none;
}
select, button {
    padding: 14px 18px;
    font-size: 45px;
    margin-top: 12px;
}
.output-box {
    width: 100%;
    height: 260px;
    background: white;
    color: black;
    font-weight: bold;
    text-shadow: 0 0 3px black;
    border: 1px solid #444;
    padding: 14px;
    margin-top: 20px;
    font-size: 40px;
    white-space: pre-wrap;
    overflow-wrap: break-word;
    word-break: break-word;
    overflow-y: scroll;
}
h2 {
    font-size: 32px;
}
</style>
</head>
<body>
<div class="container">
    <h2>My Computer 3</h2>
    <form method="post">
        <textarea id="code" name="code">{{ code }}</textarea><br>
        <select name="mode">
            <option value="python" {% if mode=='python' %}selected{% endif %}>Python</option>
            <option value="sh" {% if mode=='sh' %}selected{% endif %}>Bash</option>
            <option value="c" {% if mode=='c' %}selected{% endif %}>C</option>
            <option value="cpp" {% if mode=='cpp' %}selected{% endif %}>C++</option>
            <option value="html" {% if mode=='html' %}selected{% endif %}>HTML</option>
            <option value="js" {% if mode=='js' %}selected{% endif %}>JavaScript</option>
        </select>
        <button type="button" onclick="runCode()">Run</button>
    </form>

    <div id="output-box" class="output-box">{{ output }}</div>
</div>

<script>
const codeArea = document.getElementById("code");
const outputBox = document.getElementById("output-box");

function runCode() {
    const mode = document.querySelector("select[name='mode']").value;

    if (mode === "html" || mode === "js") {
        const blob = new Blob([codeArea.value], { type: "text/html" });
        const url = URL.createObjectURL(blob);
        window.open(url, "_blank");
        return;
    }

    // For Python, Bash, C, C++
    const form = document.createElement("form");
    form.method = "POST";

    const codeInput = document.createElement("textarea");
    codeInput.name = "code";
    codeInput.value = codeArea.value;
    form.appendChild(codeInput);

    const modeInput = document.createElement("input");
    modeInput.type = "hidden";
    modeInput.name = "mode";
    modeInput.value = mode;
    form.appendChild(modeInput);

    document.body.appendChild(form);
    form.submit();
}
</script>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    code = ""
    output = ""
    mode = "python"

    if request.method == "POST":
        code = request.form.get("code", "")
        mode = request.form.get("mode", "")

        if mode == "python":
            try:
                result = subprocess.check_output(["python3", "-c", code], stderr=subprocess.STDOUT).decode()
                output = result
            except subprocess.CalledProcessError as e:
                output = e.output.decode()

        elif mode == "sh":
            try:
                cleaned = code.replace('\r', '')
                result = subprocess.check_output(cleaned, shell=True, stderr=subprocess.STDOUT, executable="/bin/bash").decode()
                output = result
            except subprocess.CalledProcessError as e:
                output = e.output.decode()

        elif mode == "c":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".c") as tmp:
                tmp.write(code.encode())
                tmp.flush()
                exe = tmp.name + ".out"
                comp = subprocess.run(["gcc", tmp.name, "-o", exe], capture_output=True)
                if comp.returncode != 0:
                    output = comp.stderr.decode()
                else:
                    run = subprocess.run([exe], capture_output=True)
                    output = run.stdout.decode() + run.stderr.decode()
                os.unlink(tmp.name)
                if os.path.exists(exe):
                    os.unlink(exe)

        elif mode == "cpp":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".cpp") as tmp:
                tmp.write(code.encode())
                tmp.flush()
                exe = tmp.name + ".out"
                comp = subprocess.run(["g++", tmp.name, "-o", exe], capture_output=True)
                if comp.returncode != 0:
                    output = comp.stderr.decode()
                else:
                    run = subprocess.run([exe], capture_output=True)
                    output = run.stdout.decode() + run.stderr.decode()
                os.unlink(tmp.name)
                if os.path.exists(exe):
                    os.unlink(exe)

    return render_template_string(HTML, code=code, output=output, mode=mode)

if __name__ == "__main__":
    app.run(port=8000, debug=False)


