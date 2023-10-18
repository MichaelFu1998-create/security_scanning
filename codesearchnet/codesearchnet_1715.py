def quote(c):
    """Quote a single character."""
    i = ord(c)
    return ESCAPE + HEX[i//16] + HEX[i%16]