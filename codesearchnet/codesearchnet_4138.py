def encode_plus(s):
    """
    Literally encodes the plus sign
    input is a string
    returns the string with plus signs encoded
    """
    regex = r"\+"
    pat = re.compile(regex)
    return pat.sub("%2B", s)