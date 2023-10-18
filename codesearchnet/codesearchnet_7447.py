def write_py2k_header(file_list):
    """Write Python 2 shebang and add encoding cookie if needed."""
    if not isinstance(file_list, list):
        file_list = [file_list]

    python_re = re.compile(br"^(#!.*\bpython)(.*)([\r\n]+)$")
    coding_re = re.compile(br"coding[:=]\s*([-\w.]+)")
    new_line_re = re.compile(br"([\r\n]+)$")
    version_3 = LooseVersion('3')

    for file in file_list:
        if not os.path.getsize(file):
            continue

        rewrite_needed = False
        python_found = False
        coding_found = False
        lines = []

        f = open(file, 'rb')
        try:
            while len(lines) < 2:
                line = f.readline()
                match = python_re.match(line)
                if match:
                    python_found = True
                    version = LooseVersion(match.group(2).decode() or '2')
                    try:
                        version_test = version >= version_3
                    except TypeError:
                        version_test = True
                    if version_test:
                        line = python_re.sub(br"\g<1>2\g<3>", line)
                        rewrite_needed = True
                elif coding_re.search(line):
                    coding_found = True
                lines.append(line)
            if not coding_found:
                match = new_line_re.search(lines[0])
                newline = match.group(1) if match else b"\n"
                line = b"# -*- coding: utf-8 -*-" + newline
                lines.insert(1 if python_found else 0, line)
                rewrite_needed = True
            if rewrite_needed:
                lines += f.readlines()
        finally:
            f.close()

        if rewrite_needed:
            f = open(file, 'wb')
            try:
                f.writelines(lines)
            finally:
                f.close()