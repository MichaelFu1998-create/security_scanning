def parse_num(source, start, charset):
    """Returns a first index>=start of chat not in charset"""
    while start < len(source) and source[start] in charset:
        start += 1
    return start