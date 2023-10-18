def attrdict(prev, attr_names):
    """attrdict pipe can extract attribute values of object into a dict.

    The argument attr_names can be a list or a dict.

    If attr_names is a list and its item is not a valid attribute of
    prev's object. It will be excluded from yielded dict.

    If attr_names is dict and the key doesn't exist in prev's object.
    the value of corresponding attr_names key will be copy to yielded dict.

    :param prev: The previous iterator of pipe.
    :type prev: Pipe
    :param attr_names: The list or dict of attribute names
    :type attr_names: str of list or dict
    :returns: generator
    """
    if isinstance(attr_names, dict):
        for obj in prev:
            attr_values = dict()
            for name in attr_names.keys():
                if hasattr(obj, name):
                    attr_values[name] = getattr(obj, name)
                else:
                    attr_values[name] = attr_names[name]
            yield attr_values
    else:
        for obj in prev:
            attr_values = dict()
            for name in attr_names:
                if hasattr(obj, name):
                    attr_values[name] = getattr(obj, name)
            yield attr_values