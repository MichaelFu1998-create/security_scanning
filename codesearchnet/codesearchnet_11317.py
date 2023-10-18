def readfile(fn):
    """Read fn and return the contents.

    Parameters
    ----------
    fn : str
        A filename

    Returns
    -------
    str
        The content of the file

    """
    with open(path.join(HERE, fn), 'r', encoding='utf-8') as f:
        return f.read()