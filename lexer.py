def asplit(line):
    try:
        idx = line.index(' ')
    except:
        return [line]
    
    quoted = False
    split_list = [line[:idx]]
    current = ""
    while idx < len(line):
        if line[idx] == '"':
            quoted = not quoted
        elif line[idx] == "," and not quoted:
            split_list.append(current)
            current = ""
        else:
            if quoted or line[idx] != " ":
                current += line[idx]
        idx += 1
    split_list.append(current)
    return split_list