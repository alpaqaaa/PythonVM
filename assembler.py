import lexer

open("boot.bin", "wb").close()

operation_costs = {
    "VAR": 0,
    "LDI": 4,
    "LOAD": 4,
    "STORE": 4,
    "STOREI": 8,
    "COPY": 8,
    "GETC": 4,
    "JMP": 4,
    ";": 0
}

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

def label(code):
    idx = 0
    label = ""
    cost = 0
    while idx < len(code):
        line = code[idx]

        if line[0][-1] == ":":
            label = line[0][:-1]
            labels[label] = cost

        else:
            try:
                cost += operation_costs[line[0]]
            except:
                raise SyntaxError(str(idx) + ": Unknown CALL '" + line[0] + "'")
        idx += 1

def assemble(line):
    call = line[0]
    try:
        args = line[1:]
    except:
        args = []

    with open("boot.bin", "ab") as f:
        if call[-1] == ":":
            return
        match call:
            case "VAR":
                variables[args[0]] = variables["@NEXT"]
                variables["@NEXT"] += 1
            case "LDI":
                register = register_addresses[args[0]]
                value = int(args[1]) % 256
                f.write(bytes.fromhex("02" + f"{register:02X}" + f"{value:02X}" + "00"))
            case "LOAD":
                pass
            case "STORE":
                if args[0] in variables:
                    target = variables[args[0]]
                else:
                    target = int("0x" + args[0], 16)
                register = register_addresses[args[1]]
                f.write(bytes.fromhex("04" + f"{register:02X}" + f"{target%256:02X}" + f"{target>>8:02X}"))
            case "STOREI":
                target = variables[args[0]]
                value = int(args[1]) % 256
                f.write(bytes.fromhex("021a" + f"{value:02X}" + "00"))
                f.write(bytes.fromhex("041a" + f"{target%256:02X}" + f"{target>>8:02X}"))
            case "COPY":
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
            case ";":
                pass
            case _:
                raise ValueError(f"Unknown instruction: {call}")

with open("boot.pyasm", "r") as f:
    boot = f.read()

instr_list = [lexer.asplit(line) for line in boot.splitlines() if line != ""]

label(instr_list)

for line in instr_list:
    assemble(line)