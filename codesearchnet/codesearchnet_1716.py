def encode(input, output, quotetabs, header = 0):
    """Read 'input', apply quoted-printable encoding, and write to 'output'.

    'input' and 'output' are files with readline() and write() methods.
    The 'quotetabs' flag indicates whether embedded tabs and spaces should be
    quoted.  Note that line-ending tabs and spaces are always encoded, as per
    RFC 1521.
    The 'header' flag indicates whether we are encoding spaces as _ as per
    RFC 1522.
    """

    if b2a_qp is not None:
        data = input.read()
        odata = b2a_qp(data, quotetabs = quotetabs, header = header)
        output.write(odata)
        return

    def write(s, output=output, lineEnd='\n'):
        # RFC 1521 requires that the line ending in a space or tab must have
        # that trailing character encoded.
        if s and s[-1:] in ' \t':
            output.write(s[:-1] + quote(s[-1]) + lineEnd)
        elif s == '.':
            output.write(quote(s) + lineEnd)
        else:
            output.write(s + lineEnd)

    prevline = None
    while 1:
        line = input.readline()
        if not line:
            break
        outline = []
        # Strip off any readline induced trailing newline
        stripped = ''
        if line[-1:] == '\n':
            line = line[:-1]
            stripped = '\n'
        # Calculate the un-length-limited encoded line
        for c in line:
            if needsquoting(c, quotetabs, header):
                c = quote(c)
            if header and c == ' ':
                outline.append('_')
            else:
                outline.append(c)
        # First, write out the previous line
        if prevline is not None:
            write(prevline)
        # Now see if we need any soft line breaks because of RFC-imposed
        # length limitations.  Then do the thisline->prevline dance.
        thisline = EMPTYSTRING.join(outline)
        while len(thisline) > MAXLINESIZE:
            # Don't forget to include the soft line break `=' sign in the
            # length calculation!
            write(thisline[:MAXLINESIZE-1], lineEnd='=\n')
            thisline = thisline[MAXLINESIZE-1:]
        # Write out the current line
        prevline = thisline
    # Write out the last line, without a trailing newline
    if prevline is not None:
        write(prevline, lineEnd=stripped)