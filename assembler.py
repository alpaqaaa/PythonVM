import lexer

open("boot.bin", "wb").close()

variables = {
    "@NEXT": 0xe000
}

labels = {}

register_addresses = {
    "A": 0x1a,
    "B": 0x1b,
    "C": 0x1c,
    "D": 0x1d
}

def assemble(line):
    call = line[0]
    try:
        args = line[1:]
    except:
        args = []

    with open("boot.bin", "ab") as f:
        if call[-1] == ":":
            labels[call[:-1]] = 0000
        match call:
            case "PRINT":
                for char in args[0]:
                    f.write(bytes.fromhex("021a" + f"{ord(char):02X}" + "00"))
                    f.write(bytes.fromhex("041a00f0"))           
            case "PRINTCHAR":
                f.write(bytes.fromhex("021a" + f"{ord(args[0]):02X}" + "00"))
                f.write(bytes.fromhex("041a00f0"))
            case "PRINTSPACE":
                f.write(bytes.fromhex("021a2000"))
                f.write(bytes.fromhex("041a00f0"))
            case "PRINTNUM":
                value = int(args[0]) % 256
                f.write(bytes.fromhex("021a" + f"{value:02X}" + "00"))
                f.write(bytes.fromhex("041a01f0"))
            case "PRINTREG":
                reg = register_addresses[args[0]]
                f.write(bytes.fromhex("04" + f"{reg:02X}" + "00f0"))
            case "PRINTVAR":
                address = variables[args[0]]
                f.write(bytes.fromhex("031a" + f"{address%256:02X}" + f"{address>>8:02X}"))
                f.write(bytes.fromhex("041a01f0"))
            case "NEWLINE":
                f.write(bytes.fromhex("021a0a00"))
                f.write(bytes.fromhex("041a00f0"))
            case "VAR":
                variables[args[0]] = variables["@NEXT"]
                variables["@NEXT"] += 1
            case "SETVALUE":
                target = variables[args[0]]
                value = int(args[1]) % 256
                f.write(bytes.fromhex("021a" + f"{value:02X}" + "00"))
                f.write(bytes.fromhex("041a" + f"{target%256:02X}" + f"{target>>8:02X}"))
            case "ADDVALUE":
                target = variables[args[0]]
                value = int(args[1]) % 256
                f.write(bytes.fromhex("021a" + f"{value:02X}" + "00"))
                f.write(bytes.fromhex("031b" + f"{target%256:02X}" + f"{target>>8:02X}"))
                f.write(bytes.fromhex("061a1b00"))
                f.write(bytes.fromhex("041a" + f"{target%256:02X}" + f"{target>>8:02X}"))
            case "SETVAR":
                target = variables[args[0]]
                source = variables[args[1]]
                f.write(bytes.fromhex("031a" + f"{source%256:02X}" + f"{source>>8:02X}"))
                f.write(bytes.fromhex("041a" + f"{target%256:02X}" + f"{target>>8:02X}"))
            case "GETC":
                reg = register_addresses[args[0]]
                f.write(bytes.fromhex("0a" + f"{reg:02X}" + "0000"))
            case "JMP":
                target = labels[args[0]]
                f.write(bytes.fromhex("0b00" + f"{target%256:02X}" + f"{target>>8:02X}"))
            case _:
                raise ValueError(f"Unknown instruction: {call}")

with open("boot.pyasm", "r") as f:
    boot = f.read()

instr_list = [lexer.asplit(line) for line in boot.splitlines() if line != ""]

for line in instr_list:
    assemble(line)