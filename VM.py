import msvcrt, time

class VMHaltError(Exception):
    pass

def hex_pad(num):

    try:
        int(num)
    except:
        raise TypeError()

    return f"0x{num:04X}"

memory = bytearray(65536)

instruction_set = {
    0x00: "HALT",  # stop the program
    0x01: "NOP",   # no operation
    0x02: "LDI",   # load immediate value into register
    0x03: "LOAD",  # load from memory into register
    0x04: "STORE", # store register in memory
    0x05: "MOV",   # copy one register to another
    0x06: "ADD",   # add two registers together
    0x07: "SUB",   # subtract one register from another
    0x08: "MUL",   # multiply two registers together
    0x09: "DIV",   # divide one register from another
    0x0A: "GETC",  # get char input into register
    0x0B: "JMP",   # jump to address
    0x1A: "A",     # register A
    0x1B: "B",     # register B
    0x1C: "C",     # register C
    0x1D: "D"      # register D
}

registers = {
    "A": 0,
    "B": 0,
    "C": 0,
    "D": 0,
    "PC": 0x0000,
    "OF": 0
}

def updateFlags(address):
    if registers[instruction_set[address]] != registers[instruction_set[address]] & 0xff:
        registers["OF"] = 1
        registers[instruction_set[address]] &= 0xff
    else: registers["OF"] = 0 

def execute(line):
    call = instruction_set[line[0]]
    address = line[1]
    lowbyte = line[2]
    highbyte = line[3]

    match call:
        case "HALT":
            raise VMHaltError()
        case "NOP":
            registers["PC"] += 4
            return
        case "LDI":
            registers[instruction_set[address]] = (highbyte << 8) | lowbyte
        case "LOAD":
            registers[instruction_set[address]] = memory[(highbyte << 8) | lowbyte]
        case "STORE":
            if ((highbyte << 8) | lowbyte) == 0xf000:
                print(chr(registers[instruction_set[address]]), end="", flush=True)
            elif ((highbyte << 8) | lowbyte) == 0xf001:
                print(registers[instruction_set[address]], end="", flush=True)
            memory[(highbyte << 8) | lowbyte] = registers[instruction_set[address]]
        case "MOV":
            registers[instruction_set[address]] = registers[instruction_set[lowbyte]]
        case "ADD":
            registers[instruction_set[address]] += registers[instruction_set[lowbyte]]
            updateFlags(address)
        case "SUB":
            registers[instruction_set[address]] -= registers[instruction_set[lowbyte]]
            updateFlags(address)     
        case "MUL":
            registers[instruction_set[address]] *= registers[instruction_set[lowbyte]]
            updateFlags(address)
        case "DIV":
            registers[instruction_set[address]] //= registers[instruction_set[lowbyte]]
            updateFlags(address)    
        case "GETC":
            registers[instruction_set[address]] = ord(msvcrt.getch().decode('ascii'))
        case "JMP":
            registers["PC"] = (highbyte << 8) | lowbyte
            return



    registers["PC"] += 4

def cycle():
    while registers["PC"] < len(memory):
        try:
            execute(memory[registers["PC"]:registers["PC"]+4])
        except VMHaltError as e:
            print(f"HALT instruction at {hex_pad(registers["PC"])}. Program interrupted.")
            break


with open("boot.bin", "rb") as f:
    boot = f.read()
    memory[0x0000:0x0000+len(boot)] = boot

cycle()

# STRING OUTPUT BYTE: 0xf000
# NUMBER OUTPUT BYTE: 0xf001