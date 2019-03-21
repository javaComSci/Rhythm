.data

.text
.globl printx
.p2align 2
.type mngTmp,%function
.globl tjd
.p2align 2
.type mmpt,%function

manageTemplate:
        .fnstart

        mov r1, sp
        add r1, #4
        ldr r1, [r1]

        push {lr}
        mov r6, #28
        mov r9, #0
        mov r10, #0