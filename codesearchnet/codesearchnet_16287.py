def expand_macros(raw_text, macros):
    """
    this gets called before the sakefile is parsed. it looks for
    macros defined anywhere in the sakefile (the start of the line
    is '#!') and then replaces all occurences of '$variable' with the
    value defined in the macro. it then returns the contents of the
    file with the macros expanded.
    """
    includes = {}
    result = []
    pattern = re.compile("#!\s*(\w+)\s*(?:(\??\s*)=\s*(.*$)|or\s*(.*))", re.UNICODE)
    ipattern = re.compile("#<\s*(\S+)\s*(optional|or\s+(.+))?$", re.UNICODE)
    for line in raw_text.split("\n"):
        line = string.Template(line).safe_substitute(macros)
        # note that the line is appended to result before it is checked for macros
        # this prevents macros expanding into themselves
        result.append(line)
        if line.startswith("#!"):
            match = pattern.match(line)

            try:
                var, opt, val, or_ = match.group(1, 2, 3, 4)
            except:
                raise InvalidMacroError("Failed to parse macro {}\n".format(line))

            if or_:
                if var not in macros:
                    raise InvalidMacroError("Macro {} is not defined: {}\n".format(var, or_))
            elif not (opt and var in macros):
                macros[var] = val
        elif line.startswith("#<"):
            match = ipattern.match(line)
            try:
                filename = match.group(1)
            except:
                error("Failed to parse include {}\n".format(line))
                sys.exit(1)
            try:
                with io.open(filename, 'r') as f:
                    includes[filename] = expand_macros(f.read(), macros)
            except IOError:
                if match.group(2):
                    if match.group(2).startswith('or '):
                        sprint(match.group(3))
                else:
                    error("Nonexistent include {}\n".format(filename))
                    sys.exit(1)
    return "\n".join(result), includes