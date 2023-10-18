def int2fin_reference(n):
    """Calculates a checksum for a Finnish national reference number"""
    checksum = 10 - (sum([int(c) * i for c, i in zip(str(n)[::-1], it.cycle((7, 3, 1)))]) % 10)
    if checksum == 10:
        checksum = 0
    return "%s%s" % (n, checksum)