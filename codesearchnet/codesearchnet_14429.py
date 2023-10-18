def _map_arg(arg):
    """
    Return `arg` appropriately parsed or mapped to a usable value.

    """
    # Grab the easy to parse values
    if isinstance(arg, _ast.Str):
        return repr(arg.s)
    elif isinstance(arg, _ast.Num):
        return arg.n
    elif isinstance(arg, _ast.Name):
        name = arg.id
        if name == 'True':
            return True
        elif name == 'False':
            return False
        elif name == 'None':
            return None
        return name
    else:
        # Everything else we don't bother with
        return Unparseable()