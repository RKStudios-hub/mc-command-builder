def load_list(file):
    values = []
    with open(file) as f:
        for line in f:
            line = line.strip()
            if line:
                values.append(line)
    return values


def load_commands(file):
    commands = {}
    with open(file) as f:
        for line in f:
            name, syntax = line.strip().split("|")
            commands[name] = syntax
    return commands
