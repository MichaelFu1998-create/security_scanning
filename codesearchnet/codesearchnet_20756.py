def _escape_char(c, escape_char=ESCAPE_CHAR):
    """Escape a single character"""
    buf = []
    for byte in c.encode('utf8'):
        buf.append(escape_char)
        buf.append('%X' % _ord(byte))
    return ''.join(buf)