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
    background: black;
    color: #e5e5e5;
    font-family: monospace;
    margin: 0;
    padding: 0;
    display: flex;
    justify-content: left;
}

.container {
    width: 100%;
    max-width: 980px;
    padding: 25px;
}

textarea {
    width: 100%;
    height: 870px;
    font-size: 44px;
    font-weight: bold;
    background: white;
    color: black;
    border: 4px solid #777;
    padding: 14px;
    text-shadow: 0 0 2px black;
    outline: none;
}

select, button {
    padding: 8px 12px;
    font-size: 80px;
    margin-top: 12px;
}

.output-box {
    width: 100%;
    height: 1700px;
    background: white;
    color: black;
    font-weight: bold;
    border: 5px solid grey;
    padding: 14px;
    margin-top: 20px;
    font-size: 46px;
    white-space: pre-wrap;
    overflow-wrap: break-word;
    word-break: break-word;
    overflow-y: scroll;
    text-shadow: 0 0 2px black;
}

button {
    background-color: black;
    color: lightgrey;
    border: 3px solid lightgrey;
    border-radius: 12px;
    padding: 10px 14px;
    font-size: 85px;
    margin-top: 12px;
    cursor: pointer;
    transition: background-color 0.2s, color 0.2s;
}

button:hover {
    background-color: #222;
    color: #aaffaa;
    border-color: #aaffaa;
}
</style>
</head>

<body>
<div class="container">

<form method="post" id="code-form">

<textarea id="code" name="code">{{ code }}</textarea><br>

<select name="mode" id="mode">

<option value="arm64" {% if mode=='arm64' %}selected{% endif %}>ARM64</option>
<option value="c" {% if mode=='c' %}selected{% endif %}>C</option>
<option value="golang" {% if mode=='golang' %}selected{% endif %}>Golang</option>
<option value="sh" {% if mode=='sh' %}selected{% endif %}>Bash</option>
<option value="python" {% if mode=='python' %}selected{% endif %}>Python</option>
<option value="rust" {% if mode=='rust' %}selected{% endif %}>Rust</option>
<option value="php" {% if mode=='php' %}selected{% endif %}>PHP</option>
<option value="js" {% if mode=='js' %}selected{% endif %}>JavaScript</option>
<option value="html" {% if mode=='html' %}selected{% endif %}>HTML</option>

</select>

<button type="button" id="open-btn">Open</button>
<button type="button" id="save-btn">Save</button>
<button type="button" id="sys-btn">Unix</button>
<button type="button" id="clear-btn">Clear</button>
<button type="submit" id="run-btn">Run Code</button>

</form>

<input type="file" id="file-input" style="display:none;">

<div class="output-box" id="output">{{ output }}</div>

</div>

<script>
const textarea = document.getElementById('code');
const modeSelect = document.getElementById('mode');
const form = document.getElementById('code-form');
const outputBox = document.getElementById('output');
const fileInput = document.getElementById('file-input');
const openBtn = document.getElementById('open-btn');
const saveBtn = document.getElementById('save-btn');
const sysBtn = document.getElementById('sys-btn');
const clearBtn = document.getElementById('clear-btn');

form.addEventListener('submit', function(e) {
if(modeSelect.value === 'html') {
e.preventDefault();
const htmlWindow = window.open('', '_blank', 'width=1200,height=800');
htmlWindow.document.write(textarea.value);
htmlWindow.document.close();
}
});

openBtn.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', (e) => {
const file = e.target.files[0];
if (!file) return;

const reader = new FileReader();
reader.onload = function(ev) {
textarea.value = ev.target.result;
};
reader.readAsText(file);
});

saveBtn.addEventListener('click', () => {
const blob = new Blob([textarea.value], {type: 'text/plain'});
const a = document.createElement('a');
a.href = URL.createObjectURL(blob);
a.download = 'code.txt';
a.click();
URL.revokeObjectURL(a.href);
});

clearBtn.addEventListener('click', () => {
textarea.value = '';
});

sysBtn.addEventListener('click', () => {
const lines = textarea.value.split('\\n');
let caret = textarea.selectionStart;
let pos = 0;
let lineIndex = 0;

for(let i=0;i<lines.length;i++){
pos += lines[i].length + 1;
if(pos > caret){
lineIndex = i;
break;
}
}

const cmd = lines[lineIndex].trim();
if(!cmd) return;

fetch('/sys_command?cmd=' + encodeURIComponent(cmd))
.then(r => r.text())
.then(out => {
lines.splice(lineIndex+1, 0, out);
textarea.value = lines.join('\\n');
})
.catch(err => {
lines.splice(lineIndex+1, 0, 'Error: ' + err);
textarea.value = lines.join('\\n');
});
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
        if code and not code.startswith("\n"):
            code = "\n" + code
        mode = request.form.get("mode", "")

        if mode == "python":
            try:
                result = subprocess.check_output(
                    ["python3", "-c", code], stderr=subprocess.STDOUT
                ).decode()
                output = result
            except subprocess.CalledProcessError as e:
                output = e.output.decode()

        elif mode == "php":
            tmp_path = None
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".php") as tmp:
                    tmp.write(code.encode())
                    tmp_path = tmp.name

                result = subprocess.check_output(
                    ["php", tmp_path],
                    stderr=subprocess.STDOUT
                ).decode()

                output = result

            except subprocess.CalledProcessError as e:
                output = "PHP Error:\n" + e.output.decode()

            finally:
                if tmp_path and os.path.exists(tmp_path):
                    os.remove(tmp_path)

        elif mode == "rust":
            tmp_path = None
            exe_path = None
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".rs") as tmp:
                    tmp.write(code.encode())
                    tmp_path = tmp.name

                exe_path = tmp_path.replace(".rs", "")

                subprocess.check_output(
                    ["rustc", tmp_path, "-o", exe_path],
                    stderr=subprocess.STDOUT
                )

                proc = subprocess.Popen([exe_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                result, _ = proc.communicate()
                output = result.decode()

            except subprocess.CalledProcessError as e:
                output = "Rust Error:\n" + e.output.decode()

            finally:
                for path in [tmp_path, exe_path]:
                    if path and os.path.exists(path):
                        os.remove(path)

        elif mode == "sh":
            try:
                cleaned = code.replace("\r", "")
                result = subprocess.check_output(
                    cleaned,
                    shell=True,
                    stderr=subprocess.STDOUT,
                    executable="/bin/bash",
                ).decode()
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

        elif mode == "golang":
            tmp_path = None
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".go") as tmp:
                    tmp.write(code.encode())
                    tmp_path = tmp.name

                result = subprocess.check_output(
                    ["go", "run", tmp_path],
                    stderr=subprocess.STDOUT
                ).decode()

                output = result

                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

            except subprocess.CalledProcessError as e:
                output = "Go Error:\n" + e.output.decode()

                if tmp_path and os.path.exists(tmp_path):
                    os.remove(tmp_path)

        elif mode == "html":
            output = "HTML code opened in new tab."

        elif mode == "js":
            try:
                run = subprocess.check_output(
                    ["node", "-e", code], stderr=subprocess.STDOUT
                ).decode()
                output = run
            except subprocess.CalledProcessError as e:
                output = e.output.decode()

    return render_template_string(HTML, code=code, output=output, mode=mode)

@app.route("/sys_command")
def sys_command():
    cmd = request.args.get("cmd", "")

    if not cmd.strip():
        return ""

    try:
        result = subprocess.check_output(
            cmd,
            shell=True,
            stderr=subprocess.STDOUT,
            executable="/bin/bash"
        ).decode()

    except subprocess.CalledProcessError as e:
        result = e.output.decode()

    return result

if __name__ == "__main__":
    app.run(port=8800, debug=False)
