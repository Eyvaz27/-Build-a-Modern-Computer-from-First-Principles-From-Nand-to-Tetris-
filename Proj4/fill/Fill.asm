// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.


//D=A
//@addr_kbd
//M=D
//@addr_kbd
//A=M

// @SCR0
// 0; JMP;

@8192
D=A
@n
M=D
@BEGIN
0; JMP

(BEGIN)
    @i
    M=0
    @SCREEN
    D=A
    @addr_scr
    M=D
    @KBD
    D=M
    @SCR1
    D; JNE
    @SCR0
    D; JEQ
(SCR0)
    @value
    M=0
    @LOOP
    0; JMP
(SCR1)
    @value
    M=-1
    @LOOP
    0; JMP
(LOOP)
    @i
    D=M
    @n
    D=D-M
    @BEGIN
    D;JEQ
    @value
    D=M
    @addr_scr
    A=M
    M=D
    @i
    M=M+1
    @1
    D=A
    @addr_scr
    M=D+M
    @LOOP
    0;JMP
