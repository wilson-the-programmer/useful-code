import readline
import time
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style, merge_styles
from prompt_toolkit.styles.pygments import style_from_pygments_cls
from pygments.styles import get_style_by_name


aarch64_words = [
    "adc", "adcs", "add", "adds", "adr", "adrp", "and", "ands",
    "asr", "b", "b.eq", "b.ge", "b.gt", "b.hi", "b.hs", "b.le",
    "b.lo", "b.ls", "b.lt", "b.mi", "b.ne", "b.pl", "b.vs",
    "b.vc", "bic", "bics", "bl", "blr", "br", "brk", "cbnz",
    "cbz", "ccmn", "ccmp", "cinc", " cinc", "cinv", "clrex",
    "cls", "clz", "cmn", "cmp", "cneg", "csel", "cset", "csetm",
    "csinc", "csinv", "csneg", "dc", "dmb", "dsb", "dgh",
    "eon", "eor", "eret", "extr", "isb", "ldar", "ldarb",
    "ldarh", "ldaxp", "ldaxr", "ldp", "ldr", "ldrb", "ldrh",
    "ldrsb", "ldrsh", "ldrsw", "ldur", "ldurb", "ldurh",
    "ldursb", "ldursh", "ldursw", "ldxr", "ldxrb", "ldxrh",
    "lsl", "lsr", "madd", "mov", "movk", "movn", "movz",
    "msr", "mrs", "msub", "mul", "mvn", "neg", "negs",
    "nop", "orn", "orr", "prfm", "ret", "rev", "rev16",
    "rev32", "ror", "sbc", "sbcs", "sdiv", "smaddl", "smulh",
    "smull", "stlr", "stlrb", "stlrh", "stp", "str", "strb",
    "strh", "stur", "sturb", "sturh", "stxr", "stxrb",
    "stxrh", "sub", "subs", "svc", "sxtb", "sxth", "sxtw",
    "sys", "tlbi", "tst", "uxtb", "uxth", "udiv", "umaddl",
    "umulh", "umull", "wfe", "wfi", "yield"
]


aarch_64_dict = {
    "adc": ("Add values with carry", "    adc x0, x1, x2"),
    "adcs": ("Add with carry and update flags", "    adcs x0, x1, x2"),
    "add": ("Add values together", "    add x0, x1, x2"),
    "adds": ("Add values and update flags", "    adds x0, x1, x2"),
    "adr": ("Calculate address of nearby label", "    adr x1, message"),
    "adrp": ("Calculate page address of label", "    adrp x0, message"),
    "and": ("Perform bitwise AND operation", "    and x0, x1, x2"),
    "ands": ("AND values and update flags", "    ands x0, x1, x2"),
    "asr": ("Shift right preserving sign", "    asr x0, x1, #2"),
    "b": ("Branch to specified label", "    b loop"),
    "b.eq": ("Branch when values are equal", "    b.eq equal"),
    "b.ge": ("Branch when signed value is greater or equal", "    b.ge target"),
    "b.gt": ("Branch when signed value is greater", "    b.gt greater"),
    "b.hi": ("Branch when unsigned value is higher", "    b.hi target"),
    "b.hs": ("Branch when unsigned value is higher or same", "    b.hs target"),
    "b.le": ("Branch when signed value is less or equal", "    b.le target"),
    "b.lo": ("Branch when unsigned value is lower", "    b.lo target"),
    "b.ls": ("Branch when unsigned value is lower or same", "    b.ls target"),
    "b.lt": ("Branch when signed value is less", "    b.lt less"),
    "b.mi": ("Branch when negative flag is set", "    b.mi target"),
    "b.ne": ("Branch when values differ", "    b.ne different"),
    "b.pl": ("Branch when negative flag is clear", "    b.pl target"),
    "b.vc": ("Branch when overflow flag is clear", "    b.vc target"),
    "b.vs": ("Branch when overflow flag is set", "    b.vs target"),
    "bic": ("Clear selected bits using AND", "    bic x0, x1, x2"),
    "bics": ("Clear bits and update flags", "    bics x0, x1, x2"),
    "bl": ("Branch and save return address", "    bl function"),
    "blr": ("Branch to register and save return", "    blr x0"),
    "br": ("Branch to address in register", "    br x0"),
    "brk": ("Generate a breakpoint exception", "    brk #0"),
    "cbnz": ("Branch if register is nonzero", "    cbnz x0, loop"),
    "cbz": ("Branch if register equals zero", "    cbz x0, done"),
    "ccmn": ("Conditional compare negative values", "    ccmn x0, x1, #0, eq"),
    "ccmp": ("Conditional compare register values", "    ccmp x0, x1, #0, eq"),
    "cinc": ("Conditionally increment a register", "    cinc x0, x1, eq"),
    "cinv": ("Conditionally invert register bits", "    cinv x0, x1, eq"),
    "clrex": ("Clear exclusive access monitor", "    clrex"),
    "cls": ("Count leading sign bits", "    cls x0, x1"),
    "clz": ("Count leading zero bits", "    clz x0, x1"),
    "cmn": ("Compare values by adding", "    cmn x0, x1"),
    "cmp": ("Compare values and update flags", "    cmp x0, x1"),
    "cneg": ("Conditionally negate a register", "    cneg x0, x1, eq"),
    "csel": ("Select value based on condition", "    csel x0, x1, x2, eq"),
    "cset": ("Set register to zero or one", "    cset x0, eq"),
    "csetm": ("Set all bits based on condition", "    csetm x0, eq"),
    "csinc": ("Conditional select and increment", "    csinc x0, x1, x2, eq"),
    "csinv": ("Conditional select and invert", "    csinv x0, x1, x2, eq"),
    "csneg": ("Conditional select and negate", "    csneg x0, x1, x2, eq"),
    "dc": ("Perform data cache operation", "    dc cvau, x0"),
    "dgh": ("Provide data gathering hint", "    dgh"),
    "dmb": ("Order memory access operations", "    dmb ish"),
    "dsb": ("Wait for memory operations to complete", "    dsb sy"),
    "eon": ("Exclusive OR with inverted operand", "    eon x0, x1, x2"),
    "eor": ("Perform bitwise exclusive OR", "    eor x0, x1, x2"),
    "eret": ("Return from exception handler", "    eret"),
    "extr": ("Extract bits from concatenated registers", "    extr x0, x1, x2, #8"),
    "isb": ("Synchronize instruction stream", "    isb"),
    "ldar": ("Load with acquire ordering", "    ldar x0, [x1]"),
    "ldarb": ("Load byte with acquire ordering", "    ldarb w0, [x1]"),
    "ldarh": ("Load halfword with acquire ordering", "    ldarh w0, [x1]"),
    "ldaxp": ("Load pair exclusively with acquire", "    ldaxp x0, x1, [x2]"),
    "ldaxr": ("Load exclusive with acquire ordering", "    ldaxr x0, [x1]"),
    "ldp": ("Load a pair of registers", "    ldp x0, x1, [sp]"),
    "ldr": ("Load data from memory", "    ldr x0, [x1]"),
    "ldrb": ("Load one byte from memory", "    ldrb w0, [x1]"),
    "ldrh": ("Load one halfword from memory", "    ldrh w0, [x1]"),
    "ldrsb": ("Load byte and sign extend", "    ldrsb x0, [x1]"),
    "ldrsh": ("Load halfword and sign extend", "    ldrsh x0, [x1]"),
    "ldrsw": ("Load word and sign extend", "    ldrsw x0, [x1]"),
    "ldur": ("Load from unscaled memory offset", "    ldur x0, [x1, #-8]"),
    "ldurb": ("Load byte using unscaled offset", "    ldurb w0, [x1, #-1]"),
    "ldurh": ("Load halfword using unscaled offset", "    ldurh w0, [x1, #-2]"),
    "ldursb": ("Load signed byte using unscaled offset", "    ldursb x0, [x1, #-1]"),
    "ldursh": ("Load signed halfword using unscaled offset", "    ldursh x0, [x1, #-2]"),
    "ldursw": ("Load signed word using unscaled offset", "    ldursw x0, [x1, #-4]"),
    "ldxr": ("Load exclusive from memory", "    ldxr x0, [x1]"),
    "ldxrb": ("Load byte exclusively", "    ldxrb w0, [x1]"),
    "ldxrh": ("Load halfword exclusively", "    ldxrh w0, [x1]"),
    "lsl": ("Shift bits left", "    lsl x0, x1, #2"),
    "lsr": ("Shift bits right logically", "    lsr x0, x1, #2"),
    "madd": ("Multiply and add values", "    madd x0, x1, x2, x3"),
    "mov": ("Copy a value between registers", "    mov x0, #1"),
    "movk": ("Replace selected immediate bits", "    movk x0, #456, lsl #16"),
    "movn": ("Move inverted immediate value", "    movn x0, #123"),
    "movz": ("Move immediate and zero remaining bits", "    movz x0, #123"),
    "mrs": ("Read a system register", "    mrs x0, nzcv"),
    "msr": ("Write a system register", "    msr nzcv, x0"),
    "msub": ("Multiply and subtract values", "    msub x0, x1, x2, x3"),
    "mul": ("Multiply two register values", "    mul x0, x1, x2"),
    "mvn": ("Invert every bit", "    mvn x0, x1"),
    "neg": ("Negate a register value", "    neg x0, x1"),
    "negs": ("Negate and update flags", "    negs x0, x1"),
    "nop": ("Perform no operation", "    nop"),
    "orn": ("OR with inverted operand", "    orn x0, x1, x2"),
    "orr": ("Perform bitwise OR operation", "    orr x0, x1, x2"),
    "prfm": ("Prefetch data from memory", "    prfm pldl1keep, [x0]"),
    "ret": ("Return from a subroutine", "    ret"),
    "rev": ("Reverse bytes within a register", "    rev x0, x1"),
    "rev16": ("Reverse bytes within each halfword", "    rev16 x0, x1"),
    "rev32": ("Reverse bytes within each 32-bit word", "    rev32 x0, x1"),
    "ror": ("Rotate bits to the right", "    ror x0, x1, #8"),
    "sbc": ("Subtract with carry", "    sbc x0, x1, x2"),
    "sbcs": ("Subtract with carry and update flags", "    sbcs x0, x1, x2"),
    "sdiv": ("Perform signed integer division", "    sdiv x0, x1, x2"),
    "smaddl": ("Signed multiply and add long", "    smaddl x0, w1, w2, x3"),
    "smulh": ("Signed multiply high half", "    smulh x0, x1, x2"),
    "smull": ("Signed multiply and widen", "    smull x0, w1, w2"),
    "stlr": ("Store with release ordering", "    stlr x0, [x1]"),
    "stlrb": ("Store byte with release ordering", "    stlrb w0, [x1]"),
    "stlrh": ("Store halfword with release ordering", "    stlrh w0, [x1]"),
    "stp": ("Store a pair of registers", "    stp x29, x30, [sp, #-16]!"),
    "str": ("Store data into memory", "    str x0, [x1]"),
    "strb": ("Store one byte into memory", "    strb w0, [x1]"),
    "strh": ("Store one halfword into memory", "    strh w0, [x1]"),
    "stur": ("Store using unscaled memory offset", "    stur x0, [x1, #-8]"),
    "sturb": ("Store byte using unscaled offset", "    sturb w0, [x1, #-1]"),
    "sturh": ("Store halfword using unscaled offset", "    sturh w0, [x1, #-2]"),
    "stxr": ("Store exclusive to memory", "    stxr w3, x0, [x1]"),
    "stxrb": ("Store byte exclusively", "    stxrb w3, w0, [x1]"),
    "stxrh": ("Store halfword exclusively", "    stxrh w3, w0, [x1]"),
    "sub": ("Subtract one value from another", "    sub x0, x1, #1"),
    "subs": ("Subtract values and update flags", "    subs x0, x1, x2"),
    "svc": ("Generate a supervisor call exception", "    svc #0"),
    "sxtb": ("Sign extend byte to register width", "    sxtb x0, w1"),
    "sxth": ("Sign extend halfword to register width", "    sxth x0, w1"),
    "sxtw": ("Sign extend word to 64 bits", "    sxtw x0, w1"),
    "sys": ("Perform a system operation", "    sys #0, c7, c5, #0, x0"),
    "tlbi": ("Invalidate translation lookaside buffer entries", "    tlbi vmalle1"),
    "tst": ("Test bits and update flags", "    tst x0, x1"),
    "udiv": ("Perform unsigned integer division", "    udiv x0, x1, x2"),
    "umaddl": ("Unsigned multiply and add long", "    umaddl x0, w1, w2, x3"),
    "umulh": ("Unsigned multiply high half", "    umulh x0, x1, x2"),
    "umull": ("Unsigned multiply and widen", "    umull x0, w1, w2"),
    "uxtb": ("Zero extend byte to register width", "    uxtb x0, w1"),
    "uxth": ("Zero extend halfword to register width", "    uxth x0, w1"),
    "wfe": ("Wait for event", "    wfe"),
    "wfi": ("Wait for interrupt", "    wfi"),
    "yield": ("Hint that execution can yield", "    yield"),
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
