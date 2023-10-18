def _bytelist2longBigEndian(list):
    "Transform a list of characters into a list of longs."

    imax = len(list) // 4
    hl = [0] * imax

    j = 0
    i = 0
    while i < imax:
        b0 = ord(list[j]) << 24
        b1 = ord(list[j+1]) << 16
        b2 = ord(list[j+2]) << 8
        b3 = ord(list[j+3])
        hl[i] = b0 | b1 | b2 | b3
        i = i+1
        j = j+4

    return hl