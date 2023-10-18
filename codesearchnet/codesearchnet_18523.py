def get_line_count(fname):
    """Counts the number of lines in a file.

    Args:
        fname: string, name of the file.

    Returns:
        integer, the number of lines in the file.

    """
    i = 0
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1