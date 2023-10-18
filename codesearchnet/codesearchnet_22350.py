def hump_to_underscore(name):
    """
    Convert Hump style to underscore

    :param name: Hump Character
    :return: str
    """
    new_name = ''

    pos = 0
    for c in name:
        if pos == 0:
            new_name = c.lower()
        elif 65 <= ord(c) <= 90:
            new_name += '_' + c.lower()
            pass
        else:
            new_name += c
        pos += 1
        pass
    return new_name