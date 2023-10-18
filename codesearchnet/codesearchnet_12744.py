def doc(func):
    """
        Find the message shown when someone calls the help command

    Parameters
    ----------
    func : function
        the function

    Returns
    -------
    str
        The help message for this command
    """
    stripped_chars = " \t"

    if hasattr(func, '__doc__'):
        docstring = func.__doc__.lstrip(" \n\t")
        if "\n" in docstring:
            i = docstring.index("\n")
            return docstring[:i].rstrip(stripped_chars)
        elif docstring:
            return docstring.rstrip(stripped_chars)

    return ""