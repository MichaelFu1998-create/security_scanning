def readlines(filepath):
    """
    read lines from a textfile
    :param filepath:
    :return: list[line]
    """
    with open(filepath, 'rt') as f:
        lines = f.readlines()
        lines = map(str.strip, lines)
        lines = [l for l in lines if l]
    return lines