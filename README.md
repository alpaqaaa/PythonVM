# PythonVM

## Description
An 8-bit virtual machine executing binary instructions alongside an assembler converting "pyassembly" into a boot.bin file.  

## Valid assembly commands
PRINT <string>; PRINTCHAR <char/ascii code>; PRINTSPACE; PRINTNUM <number>; PRINTREG <register A/B/C/D>; PRINTVAR <variable>; NEWLINE; VAR <name>; SETVALUE <var>, <value>; ADDVALUE <var>, <value>; SETVAR <var>, <var>; GETC <register>; JMP (work in progress)

## Memory addresses
Program Counter on startup: 0x0000
String output memory address: 0xff00
Number output memory address: 0xff01
