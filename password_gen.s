.global _start

.section .data
randfile: .ascii "/dev/urandom\0"
charset: .ascii "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*_-"
charset_len = . - charset
newline: .ascii "\n"

.section .bss
randbuf: .skip 32
outbuf: .skip 32

.section .text

_start:
    mov x0, -100
    adr x1, randfile
    mov x2, 0
    mov x8, 56
    svc 0

    mov x19, x0

    mov x0, x19
    adr x1, randbuf
    mov x2, 16
    mov x8, 63
    svc 0

    mov x20, 0

loop:
    cmp x20, 16
    bge done

    adr x1, randbuf
    ldrb w2, [x1, x20]

    mov x3, charset_len
    udiv x4, x2, x3
    msub x5, x4, x3, x2

    adr x6, charset
    ldrb w7, [x6, x5]

    adr x8, outbuf
    strb w7, [x8, x20]

    add x20, x20, 1
    b loop

done:
    mov x0, 1
    adr x1, outbuf
    mov x2, 16
    mov x8, 64
    svc 0

    mov x0, 1
    adr x1, newline
    mov x2, 1
    mov x8, 64
    svc 0

    mov x0, 0
    mov x8, 93
    svc 0

