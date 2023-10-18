def attr(prev, attr_name):
    """attr pipe can extract attribute value of object.

    :param prev: The previous iterator of pipe.
    :type prev: Pipe
    :param attr_name: The name of attribute
    :type attr_name: str
    :returns: generator
    """
    for obj in prev:
        if hasattr(obj, attr_name):
            yield getattr(obj, attr_name)