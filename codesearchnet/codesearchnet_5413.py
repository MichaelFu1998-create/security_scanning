def _eval_kwargs(kwargs, my_task):
    """Parses kwargs and evaluates any Attrib entries"""
    results = {}
    for kwarg, value in list(kwargs.items()):
        if isinstance(value, Attrib) or isinstance(value, PathAttrib):
            results[kwarg] = valueof(my_task, value)
        else:
            results[kwarg] = value
    return results