.global _start
.align 2

_start: mov X0, #1
        adr X1, helloworld
        mov X2, #13
        mov X16, #4     // MacOS write system call
        svc 0
        mov     X0, #0
        mov     X16, #1
        svc     0           // terminate the program

helloworld:      .ascii  "Hello World!\n"
