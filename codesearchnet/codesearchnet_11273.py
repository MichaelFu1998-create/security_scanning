def pythonize(line, fn='', subdir='gen'):
    """Convert a line of BMPM code from PHP to Python.

    Parameters
    ----------
    line : str
        A line of code
        fn : str
        A filename
        subdir : str
        The file's subdirectory

    Returns
    -------
    The code in Python

    """
    global array_seen, nl, sd

    if '$all' in line:
        return ''
    if 'make the sum of all languages be visible in the function' in line:
        return ''

    line = line.strip()

    if 'array' in line and not line.startswith('//'):
        array_seen = True

    line = re.sub('//+', '#', line)
    # line = re.sub('"\.\((\$.+?)\)\."', r'\1', line)
    if line and re.search(r'array\("[^"]+?"\)', line):
        # print("### " + line)
        line = ''
    line = line.replace('array', '')
    line = re.sub(r'^\s*', '', line)
    line = re.sub(';$', '', line)
    line = re.sub('^include_.+', '', line)

    line = re.sub(
        r'\$(approx|rules|exact)\[LanguageIndex\("([^"]+)", '
        + r'\$languages\)\] = \$([a-zA-Z]+)',
        lambda m: (
            "BMDATA['"
            + subdir
            + "']['"
            + m.group(1)
            + "'][L_"
            + m.group(2).upper()
            + '] = _'
            + subdir.upper()
            + '_'
            + c2u(m.group(3)).upper()
        ),
        line,
    )

    line = re.sub(
        r'\$(approx|rules|exact|hebrew)([A-Za-z]+) = _merge'
        + r'\(\$([a-zA-Z]+), \$([a-zA-Z]+)\)',
        lambda m: (
            "BMDATA['"
            + subdir
            + "']['"
            + m.group(1)
            + "'][L_"
            + c2u(m.group(2)).upper()
            + '] = _'
            + subdir.upper()
            + '_'
            + c2u(m.group(3)).upper()
            + ' + _'
            + subdir.upper()
            + '_'
            + c2u(m.group(4)).upper()
        ),
        line,
    )

    line = re.sub(
        r'\$(approx|rules|exact)\[LanguageIndex\("([^"]+)", '
        + r'\$languages\)\] = _merge\(\$([a-zA-Z]+), \$([a-zA-Z]+)\)',
        lambda m: (
            "BMDATA['"
            + subdir
            + "']['"
            + m.group(1)
            + "'][L_"
            + c2u(m.group(2)).upper()
            + '] = _'
            + subdir.upper()
            + '_'
            + c2u(m.group(3)).upper()
            + ' + _'
            + subdir.upper()
            + '_'
            + c2u(m.group(4)).upper()
        ),
        line,
    )

    line = re.sub(
        r'^\$([a-zA-Z]+)',
        lambda m: '_' + sd.upper() + '_' + c2u(m.group(1)).upper(),
        line,
    )

    for _ in range(len(lang_tuple)):
        line = re.sub(r'($[a-zA-Z]+) *\+ *($[a-zA-Z]+)', r'\1\+\2', line)

    line = re.sub(
        r'\$([a-zA-Z]+)',
        lambda m: (
            'L_' + m.group(1).upper()
            if m.group(1) in lang_dict
            else '$' + m.group(1)
        ),
        line,
    )
    line = re.sub(r'\[\"\.\((L_[A-Z_+]+)\)\.\"\]', r'[\1]', line)

    line = re.sub(
        'L_([A-Z]+)', lambda m: str(lang_dict[m.group(1).lower()]), line
    )
    for _ in range(4):
        line = re.sub(
            r'([0-9]+) *\+ *([0-9]+)',
            lambda m: str(int(m.group(1)) + int(m.group(2))),
            line,
        )

    if fn == 'lang':
        if len(line.split(',')) >= 3:
            parts = line.split(',')
            parts[0] = re.sub('/(.+?)/', r'\1', parts[0])
            # parts[1] = re.sub('\$', 'L_', parts[1])
            # parts[1] = re.sub(' *\+ *', '|', parts[1])
            parts[2] = parts[2].title()
            line = ','.join(parts)

    if 'languagenames' in fn:
        line = line.replace('"', "'")
        line = line.replace("','", "', '")
        if line and line[0] == "'":
            line = ' ' * 14 + line

    # fix upstream
    # line = line.replace('ë', 'ü')

    comment = ''
    if '#' in line:
        hashsign = line.find('#')
        comment = line[hashsign:]
        code = line[:hashsign]
    else:
        code = line

    code = code.rstrip()
    comment = comment.strip()
    if not re.match(r'^\s*$', code):
        comment = '  ' + comment

    if '(' in code and ')' in code:
        prefix = code[: code.find('(') + 1]
        suffix = code[code.rfind(')') :]
        tuplecontent = code[len(prefix) : len(code) - len(suffix)]

        elts = tuplecontent.split(',')
        for i in range(len(elts)):
            elts[i] = elts[i].strip()
            if elts[i][0] == '"' and elts[i][-1] == '"':
                elts[i] = "'" + elts[i][1:-1].replace("'", "\\'") + "'"
        tuplecontent = ', '.join(elts)

        code = prefix + tuplecontent + suffix

    line = code + comment
    line = re.sub('# *', '# ', line)

    if line:
        nl = False
        if array_seen and not (line[0] == '_' or line.startswith('BMDATA')):
            line = ' ' * 4 + line
        return line + '\n'
    elif not nl:
        nl = True
        return '\n'
    else:
        return ''