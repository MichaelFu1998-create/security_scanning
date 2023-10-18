def do_escape(source, n):
    """Its actually quite complicated to cover every case :)
       http://www.javascriptkit.com/jsref/escapesequence.shtml"""
    if not n + 1 < len(source):
        return ''  # not possible here but can be possible in general case.
    if source[n + 1] in LINE_TERMINATOR:
        if source[n + 1] == CR and n + 2 < len(source) and source[n + 2] == LF:
            return source[n:n + 3], n + 3
        return source[n:n + 2], n + 2
    if source[n + 1] in ESCAPE_CHARS:
        return source[n:n + 2], n + 2
    if source[n + 1] in {'x', 'u'}:
        char, length = ('u', 4) if source[n + 1] == 'u' else ('x', 2)
        n += 2
        end = parse_num(source, n, HEX)
        if end - n < length:
            raise SyntaxError('Invalid escape sequence!')
        #if length==4:
        #    return unichr(int(source[n:n+4], 16)), n+4 # <- this was a very bad way of solving this problem :)
        return source[n - 2:n + length], n + length
    if source[n + 1] in OCTAL:
        n += 1
        end = parse_num(source, n, OCTAL)
        end = min(end, n + 3)  # cant be longer than 3
        # now the max allowed is 377 ( in octal) and 255 in decimal
        max_num = 255
        num = 0
        len_parsed = 0
        for e in source[n:end]:
            cand = 8 * num + int(e)
            if cand > max_num:
                break
            num = cand
            len_parsed += 1
        # we have to return in a different form because python may want to parse more...
        # for example '\777' will be parsed by python as a whole while js will use only \77
        return '\\' + hex(num)[1:], n + len_parsed
    return source[n + 1], n + 2