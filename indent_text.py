filename = input("Filename (e.g., test.py): ").strip()
try:
    with open(filename, "r") as f:
        lines = f.readlines()
except FileNotFoundError:
    print("File not found.")
    exit()

try:
    indent_amount = int(input("Indent space amount: ").strip())
except ValueError:
    print("Invalid number.")
    exit()

direction = input("Indent Left or Right? ").strip().lower()
if direction not in ("left", "right"):
    print("Invalid direction. Choose 'left' or 'right'.")
    exit()

new_lines = []
for line in lines:
    if direction == "right":
        new_lines.append(" " * indent_amount + line)
    else:  # left
        stripped = line.lstrip()
        # Remove up to indent_amount spaces
        removed = max(0, len(line) - len(stripped))
        spaces_to_remove = min(indent_amount, removed)
        new_lines.append(line[spaces_to_remove:])

with open(filename, "w") as f:
    f.writelines(new_lines)

print(f"File '{filename}' updated with {direction} indentation of {indent_amount} spaces.")
