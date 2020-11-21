// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

@R2
M=0

// Setting i to 0
@i
M=0

// Setting sum to 0
@sum
M=0

// Choosing small element as n
@R0
D=M
@R1
D=M-D 
@GR0
D; JGT

(GR1)
    @1
    D=M
    @n
    M=D
    @0
    D=M
    @adder
    M=D
    @LOOP
    0; JMP

(GR0)
    @0
    D=M
    @n
    M=D
    @1
    D=M
    @adder
    M=D
    @LOOP
    0; JMP

(LOOP)
    @i
    D=M+1
    @n
    D=D-M
    @SET
    D;JGT

    @adder
    D=M
    @sum
    M=M+D

    @i
    M=M+1
    @LOOP
    0;JMP

(SET)
    @sum
    D=M
    @R2
    M=D
    @END
    0;JMP
(END)
    @END
    0;JMP



