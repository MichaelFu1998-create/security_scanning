def convert_args(args, kwargs):
    """If args and kwargs contains Cells, Convert them to their values."""

    found = False
    for arg in args:
        if isinstance(arg, Cells):
            found = True
            break

    if found:
        args = tuple(
            arg.value if isinstance(arg, Cells) else arg for arg in args
        )

    if kwargs is not None:
        for key, arg in kwargs.items():
            if isinstance(arg, Cells):
                kwargs[key] = arg.value

    return args, kwargs