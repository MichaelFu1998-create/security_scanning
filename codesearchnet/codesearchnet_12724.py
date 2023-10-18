def seq_to_str(obj, sep=","):
    """
    Given a sequence convert it to a comma separated string.
    If, however, the argument is a single object, return its string
    representation.
    """
    if isinstance(obj, string_classes):
        return obj
    elif isinstance(obj, (list, tuple)):
        return sep.join([str(x) for x in obj])
    else:
        return str(obj)