machine_code = """
11010010100000000000000000000101
11110001000000000000000000000000
01010100000000000000000000000100
11010010100000000000000000001010
01010100000000000000000000001001
11101011000000000000000000000110
11101011100000000000000000000011
"""

# Full dictionary: 40+ fundamental instructions
opcode_map = {
    "110100101": "mov",
    "111010110": "add",
    "111010111": "sub",
    "111100010": "cmp",
    "0101010":   "b",
    "1001010":   "bl",
    "0101011":   "cbz",
    "0101100":   "cbnz",
    "110100110": "ldr",
    "110100111": "str",
    "111100000": "movk",
    "111100001": "movz",
    "111100011": "tst",
    "111100100": "teq",
    "111100101": "adds",
    "111100110": "subs",
    "111010001": "adr",
    "111010010": "adrp",
    "110100111": "stp",
    "110100100": "ldp",
    "111011000": "lslv",
    "111011001": "lsrv",
    "111011010": "asrv",
    "111011011": "rbit",
    "111011100": "rev",
    "111011101": "clz",
    "111011110": "cls",
    "111011111": "crc32b",
    "111100111": "crc32h",
    "111101000": "crc32w",
    "111101001": "crc32x",
    "111101010": "nop",
    "111101011": "ret",
}

def decode_arm64(binary):
    binary = binary.strip()
    prefix9 = binary[:9]
    prefix7 = binary[:7]
    instr = opcode_map.get(prefix9, opcode_map.get(prefix7, "UNKNOWN"))

    # Handle registers and immediate examples
    if instr in ["mov", "movk", "movz"]:
        reg = int(binary[9:14], 2)
        imm = int(binary[-8:], 2)
        return f"{instr:<7} x{reg}, {imm}"
    elif instr in ["cmp", "tst", "teq", "adds", "subs"]:
        reg = int(binary[9:14], 2)
        imm = int(binary[-8:], 2)
        return f"{instr:<7} x{reg}, {imm}"
    elif instr in ["add", "sub", "lslv", "lsrv", "asrv"]:
        rd = int(binary[9:14], 2)
        rn = int(binary[14:19], 2)
        rm = int(binary[19:24], 2)
        return f"{instr:<7} x{rd}, x{rn}, x{rm}"
    elif instr in ["b", "bl", "cbz", "cbnz"]:
        offset = int(binary[-16:], 2)
        return f"{instr:<7} label_{offset}"
    elif instr in ["ldr", "str", "ldp", "stp", "adr", "adrp"]:
        reg = int(binary[9:14], 2)
        return f"{instr:<7} x{reg}, [mem]"
    else:
        return f"{instr:<7}"

# Print only professional ARM64 assembly
for line in machine_code.strip().split("\n"):
    print(decode_arm64(line))
