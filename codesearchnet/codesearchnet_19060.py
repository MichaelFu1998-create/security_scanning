def to_utf8(y):
    """
    converts an array of integers to utf8 string
    """

    out = []

    for x in y:

        if x < 0x080:
            out.append(x)
        elif x < 0x0800:
            out.append((x >> 6) | 0xC0)
            out.append((x & 0x3F) | 0x80)
        elif x < 0x10000:
            out.append((x >> 12) | 0xE0)
            out.append(((x >> 6) & 0x3F) | 0x80)
            out.append((x & 0x3F) | 0x80)
        else:
            out.append((x >> 18) | 0xF0)
            out.append((x >> 12) & 0x3F)
            out.append(((x >> 6) & 0x3F) | 0x80)
            out.append((x & 0x3F) | 0x80)

    return ''.join(map(chr, out))