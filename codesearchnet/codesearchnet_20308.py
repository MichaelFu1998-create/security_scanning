def attribute_as_str(path, name):
    """Returns the two numbers found behind --[A-Z] in path. If several matches
    are found, the last one is returned.

    Parameters
    ----------
    path : string
        String with path of file/folder to get attribute from.
    name : string
        Name of attribute to get. Should be A-Z or a-z (implicit converted to
        uppercase).

    Returns
    -------
    string
        Returns two digit number found in path behind --name.
    """
    matches = re.findall('--' + name.upper() + '([0-9]{2})', path)
    if matches:
        return matches[-1]
    else:
        return None