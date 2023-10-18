def b2a_qp(data, quotetabs=False, istext=True, header=False):
    """quotetabs=True means that tab and space characters are always
       quoted.
       istext=False means that \r and \n are treated as regular characters
       header=True encodes space characters with '_' and requires
       real '_' characters to be quoted.
    """
    MAXLINESIZE = 76

    # See if this string is using CRLF line ends
    lf = data.find('\n')
    crlf = lf > 0 and data[lf-1] == '\r'

    inp = 0
    linelen = 0
    odata = []
    while inp < len(data):
        c = data[inp]
        if (c > '~' or
            c == '=' or
            (header and c == '_') or
            (c == '.' and linelen == 0 and (inp+1 == len(data) or
                                            data[inp+1] == '\n' or
                                            data[inp+1] == '\r')) or
            (not istext and (c == '\r' or c == '\n')) or
            ((c == '\t' or c == ' ') and (inp + 1 == len(data))) or
            (c <= ' ' and c != '\r' and c != '\n' and
             (quotetabs or (not quotetabs and (c != '\t' and c != ' '))))):
            linelen += 3
            if linelen >= MAXLINESIZE:
                odata.append('=')
                if crlf: odata.append('\r')
                odata.append('\n')
                linelen = 3
            odata.append('=' + two_hex_digits(ord(c)))
            inp += 1
        else:
            if (istext and
                (c == '\n' or (inp+1 < len(data) and c == '\r' and
                               data[inp+1] == '\n'))):
                linelen = 0
                # Protect against whitespace on end of line
                if (len(odata) > 0 and
                    (odata[-1] == ' ' or odata[-1] == '\t')):
                    ch = ord(odata[-1])
                    odata[-1] = '='
                    odata.append(two_hex_digits(ch))

                if crlf: odata.append('\r')
                odata.append('\n')
                if c == '\r':
                    inp += 2
                else:
                    inp += 1
            else:
                if (inp + 1 < len(data) and
                    data[inp+1] != '\n' and
                    (linelen + 1) >= MAXLINESIZE):
                    odata.append('=')
                    if crlf: odata.append('\r')
                    odata.append('\n')
                    linelen = 0

                linelen += 1
                if header and c == ' ':
                    c = '_'
                odata.append(c)
                inp += 1
    return ''.join(odata)