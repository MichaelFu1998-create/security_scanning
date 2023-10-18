def alter_freevars(func, globals_=None, **vars):
    """Replace local variables with free variables

    Warnings:
        This function does not work.
    """

    if globals_ is None:
        globals_ = func.__globals__

    frees = tuple(vars.keys())
    oldlocs = func.__code__.co_names
    newlocs = tuple(name for name in oldlocs if name not in frees)

    code = _alter_code(func.__code__,
                       co_freevars=frees,
                       co_names=newlocs,
                       co_flags=func.__code__.co_flags | inspect.CO_NESTED)
    closure = _create_closure(*vars.values())

    return FunctionType(code, globals_, closure=closure)