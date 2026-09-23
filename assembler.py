open("boot.bin", "wb").close()

variables = {
    "@NEXT": 0xe000
}

register_addresses = {
    "A": 0x1a,
    "B": 0x1b,
    "C": 0x1c,
    "D": 0x1d
}

def assemble(line):
    split = line.split(' ')
    call = split[0]
    try:
        args = split[1:]
    except:
        args = []

    with open("boot.bin", "ab") as f:
        match call:
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
                f.write(bytes.fromhex("04" + str(reg) + "00f0"))
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
            case "SETVAR":
                target = variables[args[0]]
                source = variables[args[1]]
                f.write(bytes.fromhex("031a" + f"{source%256:02X}" + f"{source>>8:02X}"))
                f.write(bytes.fromhex("041a" + f"{target%256:02X}" + f"{target>>8:02X}"))
            case "GETC":
                f.write(bytes.fromhex("0a1a0000"))


boot = """
GETC A
PRINTREG A
"""

instr_list = [line for line in boot.splitlines() if line != ""]

for line in instr_list:
    assemble(line)