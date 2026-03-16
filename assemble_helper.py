import os
import time
from pathlib import Path


next_offset = 0


print("Welcome to Python → ARM64 converter!")
time.sleep(1)
file_name = input("Enter your Python file name (e.g., test.py): ").strip()

path = Path(file_name)
if not path.is_file():
    print(f"File {file_name} not found!")
else:
    asm_lines = [
        ".section .data",
        ".section .bss",
        "vars: .space 128",
        "buf: .space 256",
        ".section .text",
        ".global _start",
        "_start:"
    ]

    variables = {}


    def get_offset(var):
        global next_offset
        if var not in variables:
            variables[var] = next_offset
            next_offset += 8
        return variables[var]

    with open(file_name) as f:
        code_lines = f.read().splitlines()

    for line in code_lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Assignment (numbers)
        if '=' in line and '+' not in line:
            var, value = map(str.strip, line.split('='))
            offset = get_offset(var)
            asm_lines.append(f"    mov x0, {value}")
            asm_lines.append(f"    adr x1, vars")
            asm_lines.append(f"    str x0, [x1, #{offset}]    // {var} = {value}")

        # Addition
        elif '=' in line and '+' in line:
            var, expr = map(str.strip, line.split('='))
            op1, op2 = map(str.strip, expr.split('+'))
            offset_dest = get_offset(var)

            # load first operand
            if op1.isalpha():
                off1 = get_offset(op1)
                asm_lines.append(f"    adr x1, vars")
                asm_lines.append(f"    ldr x1, [x1, #{off1}]")
                op1_reg = "x1"
            else:
                asm_lines.append(f"    mov x1, {op1}")
                op1_reg = "x1"

            # load second operand
            if op2.isalpha():
                off2 = get_offset(op2)
                asm_lines.append(f"    adr x2, vars")
                asm_lines.append(f"    ldr x2, [x2, #{off2}]")
                op2_reg = "x2"
            else:
                asm_lines.append(f"    mov x2, {op2}")
                op2_reg = "x2"

            asm_lines.append(f"    add x0, {op1_reg}, {op2_reg}")
            asm_lines.append(f"    adr x1, vars")
            asm_lines.append(f"    str x0, [x1, #{offset_dest}]    // {var} = {op1} + {op2}")

        # Print
        elif line.startswith("print("):
            val = line[6:-1].strip()
            if val.startswith('"') and val.endswith('"'):
                string_val = val[1:-1].replace('\\n', '\n').replace('\\t', '\t')
                asm_lines.append("    adr x1, buf")
                for i, ch in enumerate(string_val):
                    asm_lines.append(f"    mov w0, #{ord(ch)}")
                    asm_lines.append(f"    strb w0, [x1, #{i}]")
                asm_lines.append("    mov x0, 1")
                asm_lines.append("    adr x1, buf")
                asm_lines.append(f"    mov x2, {len(string_val)}")
                asm_lines.append("    mov x8, 64")
                asm_lines.append("    svc 0")
            else:
                if val.isdigit():
                    asm_lines.append(f"    mov x0, {val}")
                else:
                    off = get_offset(val)
                    asm_lines.append(f"    adr x1, vars")
                    asm_lines.append(f"    ldr x0, [x1, #{off}]")

                # convert number to ASCII and print
                asm_lines.append("    adr x1, buf")
                asm_lines.append("    mov x2, 10")
                asm_lines.append("    mov x3, 0")
                asm_lines.append("convert:")
                asm_lines.append("        udiv x4, x0, x2")
                asm_lines.append("        msub x5, x4, x2, x0")
                asm_lines.append("        add x5, x5, '0'")
                asm_lines.append("        strb w5, [x1, x3]")
                asm_lines.append("        add x3, x3, 1")
                asm_lines.append("        mov x0, x4")
                asm_lines.append("        cbnz x0, convert")
                asm_lines.append("    mov x0, 1")
                asm_lines.append("    adr x1, buf")
                asm_lines.append("    mov x2, x3")
                asm_lines.append("    mov x8, 64")
                asm_lines.append("    svc 0")

    asm_lines.append("    mov x0, 0")
    asm_lines.append("    mov x8, 93")
    asm_lines.append("    svc 0")

    print("\nGenerated ARM64 assembly:\n")
    print("\n".join(asm_lines))

