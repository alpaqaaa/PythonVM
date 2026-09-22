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
    0x00: "HALT",
    0x01: "NOP",
    0x02: "LDI",
    0x03: "STORE",
    0x04: "MOV",
    0x05: "ADD",
    0x0A: "A",
    0x0B: "B",
    0x0C: "C",
    0x0D: "D"
}

registers = {
    "A": 0,
    "B": 0,
    "C": 0,
    "D": 0,
    "PC": 0x0000
}

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
                print(chr(registers[instruction_set[address]]), end="")
                registers["PC"] += 4
                return
            elif ((highbyte << 8) | lowbyte) == 0xf001:
                print(registers[instruction_set[address]], end="")
            memory[(highbyte << 8) | lowbyte] = registers[instruction_set[address]]
        case "MOV":
            registers[instruction_set[address]] = registers[instruction_set[lowbyte]]
        case "ADD":
            registers[instruction_set[address]] += registers[instruction_set[lowbyte]]
            registers[instruction_set[address]] &= 0xff
        case "SUB":
            registers[instruction_set[address]] -= registers[instruction_set[lowbyte]]
            registers[instruction_set[address]] &= 0xff       
        case "MUL":
            registers[instruction_set[address]] *= registers[instruction_set[lowbyte]]
            registers[instruction_set[address]] &= 0xff 
        case "DIV":
            registers[instruction_set[address]] //= registers[instruction_set[lowbyte]]
            registers[instruction_set[address]] &= 0xff              


    registers["PC"] += 4


def cycle():
    while registers["PC"] < len(memory):
        try:
            execute(memory[registers["PC"]:registers["PC"]+4])
        except VMHaltError as e:
            print(f"HALT instruction at {hex_pad(registers["PC"])}. Program interrupted.")
            break

boot = [
"02", "0a", "49", "00", # LDI A, 73 = "I"
"03", "0a", "00", "f0", # STORE A, 0xf000
"02", "0a", "63", "00", # LDI A, 99 = "c"
"03", "0a", "00", "f0", # STORE A, 0xf000
"02", "0a", "68", "00", # LDI A, 104 = "h"
"03", "0a", "00", "f0", # STORE A, 0xf000
]

memory[0x0000:0x0000+len(boot)] = bytes.fromhex(''.join(boot))

cycle()

# STRING OUTPUT BYTE: 0xf000
# NUMBER OUTPUT BYTE: 0xf001