import subprocess
import os
from time import sleep
import my_github_data

from prompt_toolkit.shortcuts import input_dialog


YELLOW = "\033[1;38;2;255;255;0m"
ORANGE = "\033[1;38;2;255;165;0m"
CYAN   = "\033[1;38;2;0;255;255m"
BEIGE  = "\033[1;38;2;245;245;220m"
RESET  = "\033[0m"

print(f"\n\n{YELLOW}Welcome to Quick GitHub Push!{RESET}\n\n")
sleep(2)
#file_name = input("Filename: ").strip()

file_name = input_dialog(title="File to Push to GitHub", text="File").run()
if file_name:
    file_name = file_name.strip()


if not os.path.isfile(file_name):
    print(f"Error: {file_name} does not exist in the current directory.")
    exit(1)

repo_url = f"https://{my_github_data.GITHUB_USER}:{my_github_data.ACCESS_TOKEN}@github.com/{my_github_data.GITHUB_USER}/{my_github_data.REPO_NAME}.git"

if not os.path.isdir(".git"):
    subprocess.run(["git", "init"])
    subprocess.run(["git", "remote", "add", "origin", repo_url])

subprocess.run(["git", "config", "user.name", my_github_data.GITHUB_USER])
subprocess.run(["git", "config", "user.email", my_github_data.GITHUB_USER])

subprocess.run(["git", "add", file_name])
subprocess.run(["git", "commit", "-m", f"Add {file_name}"])
subprocess.run(["git", "branch", "-M", "main"])
subprocess.run(["git", "pull", "origin", "main", "--rebase"])
subprocess.run(["git", "push", "-u", "origin", "main"])

print(f"\n✅ {file_name} has been pushed to https://github.com/{my_github_data.GITHUB_USER}/{my_github_data.REPO_NAME}")
