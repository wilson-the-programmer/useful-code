"""
Assemble, link and run Assembly ARM64 file
"""
import os

try:
    file_name = input("ARM64 file (ex: hello.s)\n\n: ").strip()

    if not os.path.exists(file_name):
        print("File does not exist.")
    else:
        base = file_name.replace(".s", "")

        assemble = f"as -o {base}.o {file_name}"
        link = f"ld -o {base} {base}.o"
        run = f"./{base}"

        os.system(assemble)
        os.system(link)
        os.system(run)

except Exception as e:
    print(e)

