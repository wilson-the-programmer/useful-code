import subprocess
import os
import shutil
from time import sleep
import my_github_data


print("\nWelcome to Quick GitHub Push!\n")
sleep(1)

file_name = input("File to push: ").strip()

if not os.path.isfile(file_name):
    print(f"Error: {file_name} does not exist.")
    exit(1)

repo_name = input("GitHub repository name: ").strip()

if not repo_name:
    print("Error: repository name required.")
    exit(1)

if os.path.isdir(".git"):
    shutil.rmtree(".git")

repo_url = (
    f"https://{my_github_data.GITHUB_USER}:"
    f"{my_github_data.ACCESS_TOKEN}@github.com/"
    f"{my_github_data.GITHUB_USER}/{repo_name}.git"
)

subprocess.run(["git", "init"], check=True)
subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)
subprocess.run(["git", "config", "user.name", my_github_data.GITHUB_USER], check=True)
subprocess.run(
    ["git", "config", "user.email", f"{my_github_data.GITHUB_USER}@users.noreply.github.com"],
    check=True
)

subprocess.run(["git", "add", file_name], check=True)
subprocess.run(["git", "commit", "-m", f"Add {file_name}"], check=True)
subprocess.run(["git", "branch", "-M", "main"], check=True)
subprocess.run(["git", "push", "-u", "origin", "main", "--force"], check=True)

print(f"\n{file_name} pushed to https://github.com/{my_github_data.GITHUB_USER}/{repo_name}")


