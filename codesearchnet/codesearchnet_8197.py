def load(file, use_yaml=None):
    """
    Loads not only JSON files but also YAML files ending in .yml.

    :param file: a filename or file handle to read from
    :returns: the data loaded from the JSON or YAML file
    :rtype: dict
    """
    if isinstance(file, str):
        fp = open(file)
        filename = file
    else:
        fp = file
        filename = getattr(fp, 'name', '')

    try:
        return loads(fp.read(), use_yaml, filename)

    except Exception as e:
        e.args = ('There was a error in the data file', filename) + e.args
        raise