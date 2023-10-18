def unhex(s):
    """Get the integer value of a hexadecimal number."""
    bits = 0
    for c in s:
        if '0' <= c <= '9':
            i = ord('0')
        elif 'a' <= c <= 'f':
            i = ord('a')-10
        elif 'A' <= c <= 'F':
            i = ord('A')-10
        else:
            break
        bits = bits*16 + (ord(c) - i)
    return bits