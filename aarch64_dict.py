import readline
import time
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style, merge_styles
from prompt_toolkit.styles.pygments import style_from_pygments_cls
from pygments.styles import get_style_by_name


aarch64_words = [
    "mov", "movz", "movk", "ldr", "str", "ldp", "stp", "adr", "adrp",
    "add", "sub", "mul", "madd", "msub", "sdiv", "udiv", "neg",
    "and", "orr", "eor", "mvn", "lsl", "lsr", "asr", "cmp", "tst",
    "b", "bl", "br", "blr", "ret", "cbz", "cbnz", "b.eq", "b.ne",
    "b.gt", "b.lt", "svc", "nop", "csel", "cset", "mrs", "msr",
    "exit", "quit"
]


aarch_64_dict = {
    "mov": ("Copy a value between registers", "    mov x0, #1"),
    "movz": ("Move immediate and zero remaining bits", "    movz x0, #123"),
    "movk": ("Replace selected immediate bits", "    movk x0, #456, lsl #16"),
    "ldr": ("Load data from memory", "    ldr x0, [x1]"),
    "str": ("Store data into memory", "    str x0, [x1]"),
    "ldp": ("Load a pair of registers", "    ldp x0, x1, [sp]"),
    "stp": ("Store a pair of registers", "    stp x29, x30, [sp, #-16]!"),
    "adr": ("Calculate address of nearby label", "    adr x1, message"),
    "adrp": ("Calculate page address of label", "    adrp x0, message"),
    "add": ("Add values together", "    add x0, x1, x2"),
    "sub": ("Subtract one value from another", "    sub x0, x1, #1"),
    "mul": ("Multiply two register values", "    mul x0, x1, x2"),
    "madd": ("Multiply and add values", "    madd x0, x1, x2, x3"),
    "msub": ("Multiply and subtract values", "    msub x0, x1, x2, x3"),
    "sdiv": ("Perform signed integer division", "    sdiv x0, x1, x2"),
    "udiv": ("Perform unsigned integer division", "    udiv x0, x1, x2"),
    "neg": ("Negate a register value", "    neg x0, x1"),
    "and": ("Perform bitwise AND operation", "    and x0, x1, x2"),
    "orr": ("Perform bitwise OR operation", "    orr x0, x1, x2"),
    "eor": ("Perform bitwise exclusive OR", "    eor x0, x1, x2"),
    "mvn": ("Invert every bit", "    mvn x0, x1"),
    "lsl": ("Shift bits left", "    lsl x0, x1, #2"),
    "lsr": ("Shift bits right logically", "    lsr x0, x1, #2"),
    "asr": ("Shift right preserving sign", "    asr x0, x1, #2"),
    "cmp": ("Compare values and update flags", "    cmp x0, x1"),
    "tst": ("Test bits and update flags", "    tst x0, x1"),
    "b": ("Branch to specified label", "    b loop"),
    "bl": ("Branch and save return address", "    bl function"),
    "br": ("Branch to address in register", "    br x0"),
    "blr": ("Branch to register and save return", "    blr x0"),
    "ret": ("Return from a subroutine", "    ret"),
    "cbz": ("Branch if register equals zero", "    cbz x0, done"),
    "cbnz": ("Branch if register is nonzero", "    cbnz x0, loop"),
    "b.eq": ("Branch when values are equal", "    b.eq equal"),
    "b.ne": ("Branch when values differ", "    b.ne different"),
    "b.gt": ("Branch when signed value is greater", "    b.gt greater"),
    "b.lt": ("Branch when signed value is less", "    b.lt less"),
    "svc": ("Generate a supervisor call exception", "    svc #0"),
    "nop": ("Perform no operation", "    nop"),
    "csel": ("Select value based on condition", "    csel x0, x1, x2, eq"),
    "cset": ("Set register to zero or one", "    cset x0, eq"),
    "mrs": ("Read a system register", "    mrs x0, nzcv"),
    "msr": ("Write a system register", "    msr nzcv, x0"),
}


one_dark_style = style_from_pygments_cls(
    get_style_by_name("one-dark")
)


completion_style = Style.from_dict({
    "prompt": "bold #ffa500",
    "": "#cccccc",
    "completion-menu.completion": "bg:#111155 #ffffff",
    "completion-menu.completion.current": "bg:#00aaaa #000000",
    "scrollbar.background": "bg:#88aaaa",
    "scrollbar.button": "bg:#222222",
})


style = merge_styles([
    one_dark_style,
    completion_style
])


def get_completer():
    return WordCompleter(
        aarch64_words,
        ignore_case=True
    )


def aarch64_decode(instruction):
    instruction = instruction.strip().lower()

    if not instruction:
        return None

    instruction = instruction.split()[0]

    if instruction in aarch_64_dict:
        description, example = aarch_64_dict[instruction]
        return f"{description}\n\nExample:\n_start:\n{example}"

    return "Instruction not found"


def main():
    print("AArch64 Instruction Dictionary\n")
    print("Type an instruction to look it up.")
    print("Type exit to quit.\n")

    session = PromptSession(
        style=style,
        auto_suggest=AutoSuggestFromHistory()
    )

    while True:
        try:
            instruction = session.prompt(
                [("class:prompt", "\nAArch64> ")],
                completer=get_completer()
            )

            instruction = instruction.strip()

            if instruction.lower() in ("exit", "quit"):
                break

            result = aarch64_decode(instruction)

            if result:
                time.sleep(0.4)
                print(result)

        except (KeyboardInterrupt, EOFError):
            print()
            break

    print("Goodbye!")


if __name__ == "__main__":
    main()
