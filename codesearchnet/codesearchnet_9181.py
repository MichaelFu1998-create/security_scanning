def hex_to_rgb(value):
    """
    Convert the given hex string to a
    valid RGB channel triplet.
    """
    value = value.lstrip('#')
    check_hex(value)

    length = len(value)
    step = int(length / 3)
    return tuple(int(value[i:i+step], 16) for i in range(0, length, step))