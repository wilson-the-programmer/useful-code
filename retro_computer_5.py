from flask import Flask, request, render_template_string
import subprocess
import tempfile
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>My Computer 3</title>
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
    <form method="post" id="code-form">
        <textarea name="code">{{ code }}</textarea><br>
        <select name="mode">
            <option value="python" {% if mode=='python' %}selected{% endif %}>Python</option>
            <option value="sh" {% if mode=='sh' %}selected{% endif %}>Bash</option>
            <option value="c" {% if mode=='c' %}selected{% endif %}>C</option>
            <option value="cpp" {% if mode=='cpp' %}selected{% endif %}>C++</option>
            <option value="html" {% if mode=='html' %}selected{% endif %}>HTML</option>
            <option value="js" {% if mode=='js' %}selected{% endif %}>JavaScript</option>
        </select>
        <button type="submit" id="run-btn">Run</button>
    </form>

    <div class="output-box" id="output">{{ output }}</div>

</div>

<script>
const form = document.getElementById('code-form');
const outputBox = document.getElementById('output');

form.addEventListener('submit', function(e) {
    const mode = form.mode.value;
    if(mode === 'html') {
        e.preventDefault();
        const htmlWindow = window.open('', '_blank');
        htmlWindow.document.write(form.code.value);
        htmlWindow.document.close();
    }
});
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

        elif mode == "html":
            output = "HTML code opened in new tab."

        elif mode == "js":
            try:
                run = subprocess.check_output(["node", "-e", code], stderr=subprocess.STDOUT).decode()
                output = run
            except subprocess.CalledProcessError as e:
                output = e.output.decode()

    return render_template_string(HTML, code=code, output=output, mode=mode)

if __name__ == "__main__":
    app.run(port=8000, debug=False)


