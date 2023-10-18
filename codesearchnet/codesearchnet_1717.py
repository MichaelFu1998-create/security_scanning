def decode(input, output, header = 0):
    """Read 'input', apply quoted-printable decoding, and write to 'output'.
    'input' and 'output' are files with readline() and write() methods.
    If 'header' is true, decode underscore as space (per RFC 1522)."""

    if a2b_qp is not None:
        data = input.read()
        odata = a2b_qp(data, header = header)
        output.write(odata)
        return

    new = ''
    while 1:
        line = input.readline()
        if not line: break
        i, n = 0, len(line)
        if n > 0 and line[n-1] == '\n':
            partial = 0; n = n-1
            # Strip trailing whitespace
            while n > 0 and line[n-1] in " \t\r":
                n = n-1
        else:
            partial = 1
        while i < n:
            c = line[i]
            if c == '_' and header:
                new = new + ' '; i = i+1
            elif c != ESCAPE:
                new = new + c; i = i+1
            elif i+1 == n and not partial:
                partial = 1; break
            elif i+1 < n and line[i+1] == ESCAPE:
                new = new + ESCAPE; i = i+2
            elif i+2 < n and ishex(line[i+1]) and ishex(line[i+2]):
                new = new + chr(unhex(line[i+1:i+3])); i = i+3
            else: # Bad escape sequence -- leave it in
                new = new + c; i = i+1
        if not partial:
            output.write(new + '\n')
            new = ''
    if new:
        output.write(new)