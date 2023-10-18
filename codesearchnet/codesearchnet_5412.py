def _eval_args(args, my_task):
    """Parses args and evaluates any Attrib entries"""
    results = []
    for arg in args:
        if isinstance(arg, Attrib) or isinstance(arg, PathAttrib):
            results.append(valueof(my_task, arg))
        else:
            results.append(arg)
    return results