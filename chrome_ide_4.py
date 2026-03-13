from flask import Flask, request
import subprocess
import sys
import io
import tempfile
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    code = ""
    output = ""

    if request.method == 'POST':
        code = request.form.get('code', '')
        mode = request.form.get('mode', '')

        if mode == 'python':
            try:
                old_stdout = sys.stdout
                redirected_output = sys.stdout = io.StringIO()
                exec(code, {})
                output = redirected_output.getvalue()
                sys.stdout = old_stdout
            except Exception as e:
                output = f"Python Error: {e}"

        elif mode == 'javascript':
            try:
                result = subprocess.check_output(
                    ["node", "-e", code],
                    stderr=subprocess.STDOUT
                ).decode()
                output = result
            except subprocess.CalledProcessError as e:
                output = "JavaScript Error:\n" + e.output.decode()

        elif mode == "bash":

            code = code.replace("\r\n", "\n").replace("\r", "\n")

            with tempfile.NamedTemporaryFile(delete=False, suffix=".sh", mode="w") as f:
                f.write(code)
                path = f.name

            try:
                result = subprocess.check_output(
                    ["bash", path],
                    stderr=subprocess.STDOUT
                ).decode()

                output = result

            except subprocess.CalledProcessError as e:
                output = e.output.decode()

            finally:
                os.remove(path)


        elif mode == 'c':
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".c") as tmp:
                    tmp.write(code.encode())
                    tmp_path = tmp.name
                    exe_path = tmp_path + ".out"

                subprocess.check_output(
                    ["gcc", tmp_path, "-o", exe_path],
                    stderr=subprocess.STDOUT
                )
                result = subprocess.check_output([exe_path], stderr=subprocess.STDOUT).decode()
                output = result
                os.remove(tmp_path)
                os.remove(exe_path)
            except subprocess.CalledProcessError as e:
                output = "C Error:\n" + e.output.decode()
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
                if os.path.exists(exe_path):
                    os.remove(exe_path)

        elif mode == 'cpp':
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".cpp") as tmp:
                    tmp.write(code.encode())
                    tmp_path = tmp.name
                    exe_path = tmp_path + ".out"

                subprocess.check_output(
                    ["g++", tmp_path, "-o", exe_path],
                    stderr=subprocess.STDOUT
                )
                result = subprocess.check_output([exe_path], stderr=subprocess.STDOUT).decode()
                output = result
                os.remove(tmp_path)
                os.remove(exe_path)
            except subprocess.CalledProcessError as e:
                output = "C++ Error:\n" + e.output.decode()
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
                if os.path.exists(exe_path):
                    os.remove(exe_path)

        elif mode == 'golang':
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".go") as tmp:
                    tmp.write(code.encode())
                    tmp_path = tmp.name

                result = subprocess.check_output(
                    ["go", "run", tmp_path],
                    stderr=subprocess.STDOUT
                ).decode()

                output = result
                os.remove(tmp_path)
            except subprocess.CalledProcessError as e:
                output = "Go Error:\n" + e.output.decode()
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

        elif mode == 'rustc':
            try:
                with tempfile.TemporaryDirectory() as tmpdir:
                    rs_file = os.path.join(tmpdir, "main.rs")
                    exe_file = os.path.join(tmpdir, "main_exe")
                    with open(rs_file, "w") as f:
                        f.write(code)
                    subprocess.check_output(["rustc", rs_file, "-o", exe_file], stderr=subprocess.STDOUT)
                    result = subprocess.check_output([exe_file], stderr=subprocess.STDOUT).decode()
                    output = result
            except subprocess.CalledProcessError as e:
                output = "Rust Error:\n" + e.output.decode()

    return f'''
    <html>
    <head>
        <title>Code Runner</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/codemirror.min.css">
        <link id="cm-theme-css" rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/theme/abcdef.min.css">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/codemirror.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/mode/python/python.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/mode/javascript/javascript.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/mode/clike/clike.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/mode/rust/rust.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/mode/go/go.min.js"></script>
        <style>
            body {{
                background-color: black;
                color: lightgrey;
                font-family: monospace;
                padding: 10px;
            }}
            .CodeMirror {{
                height: 850px;
                0px;
                width: 95%;
                padding: 20px;
                border: 6px outset #222;
                background: #000;
                color: lightgrey;
            }}
            .CodeMirror pre {{
                font-size: 42px !important;
                font-weight: bold !important;
                line-height: 1.4 !important;
                font-family: monospace;
            }}
            .CodeMirror-linenumber {{
                font-size: 42px !important;
                font-weight: bold !important;
                line-height: 1.4 !important;
            }}
            #output {{
                width: 100%;
                height: 45em;
                font-size: 42px;
                font-weight: bold;
                text-shadow: 0 0 3px black;
                font-family: monospace;
                background-color: white;
                color: black;
                border: 12px solid grey;
                overflow-x: auto;
                white-space: pre-wrap;
                margin-top: 10px;
                padding: 12px;
                box-sizing: border-box;
            }}
            .button-row {{
                display: flex;
                gap: 7px;
                margin-bottom: 14px;
                margin-top: 14px
            }}
            button.code-btn {{
                font-family: monospace;
                font-weight: bold;
                font-size: 36px;
                padding: 15px 0;
                background-color: #000;
                color: lightgrey;
                border: 14px outset lightgrey;
                cursor: pointer;
                flex: 1;
                min-width: 0;
                height: 130px;
            }}
        </style>
    </head>
    <body>
        <form method="POST" id="code-form">
            <textarea id="code" name="code" spellcheck="false">{code}</textarea><br>

            <div class="button-row">
                <button class="code-btn" type="button" onclick="runCode('bash','null')">Bash</button>
                <button class="code-btn" type="button" onclick="runCode('c','text/x-csrc')">C</button>
                <button class="code-btn" type="button" onclick="runCode('cpp','text/x-c++src')">C++</button>
                <button class="code-btn" type="button" onclick="runCode('golang','go')">Go</button>
                <button class="code-btn" type="button" onclick="runCode('rustc','rust')">Rustc</button>
            </div>

            <div class="button-row">
                <button class="code-btn" type="button" onclick="runCode('python','python')">Python</button>
                <button class="code-btn" type="button" onclick="runCode('javascript','javascript')">JS</button>
                <button class="code-btn" type="button" onclick="fullView()">HTML</button>
                <button class="code-btn" type="button" onclick="saveFile()">Save</button>
                <button class="code-btn" type="button" onclick="clearEditor()">Clear</button>
            </div>

            <textarea id="output" >{output}</textarea>
        </form>

        <script>
            const editor = CodeMirror.fromTextArea(document.getElementById('code'), {{
                mode: "python",
                lineNumbers:false,
                matchBrackets: true,
                autoCloseBrackets: true,
                theme: "abcdef",
                tabSize: 4,
                lineWrapping: true
            }});
            editor.refresh();

            let allowUnload = false;
            window.addEventListener("beforeunload", function(e) {{
                if (!allowUnload) {{
                    e.preventDefault();
                    e.returnValue = "";
                }}
            }});

            function runCode(mode, cmMode) {{
                if (cmMode !== "null") {{
                    editor.setOption("mode", cmMode);
                }}
                allowUnload = true;
                const form = document.getElementById("code-form");
                const input = document.createElement("input");
                input.type = "hidden";
                input.name = "mode";
                input.value = mode;
                form.appendChild(input);
                form.submit();
            }}

            function fullView() {{
                const code = editor.getValue();
                const blob = new Blob([code], {{ type: 'text/html' }});
                const url = URL.createObjectURL(blob);
                window.open(url, '_blank');
            }}

            function saveFile() {{
                const code = editor.getValue();
                const blob = new Blob([code], {{ type: 'text/plain' }});
                const a = document.createElement('a');
                a.href = URL.createObjectURL(blob);
                a.download = "code.txt";
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
            }}

            function clearEditor() {{
                editor.setValue("");
            }}
        </script>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(port=8700, debug=False)
    
