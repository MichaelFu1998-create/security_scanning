def attrs(prev, attr_names):
    """attrs pipe can extract attribute values of object.

    If attr_names is a list and its item is not a valid attribute of
    prev's object. It will be excluded from yielded dict.

    :param prev: The previous iterator of pipe.
    :type prev: Pipe
    :param attr_names: The list of attribute names
    :type attr_names: str of list
    :returns: generator
    """
    for obj in prev:
        attr_values = []
        for name in attr_names:
            if hasattr(obj, name):
                attr_values.append(getattr(obj, name))
        yield attr_values