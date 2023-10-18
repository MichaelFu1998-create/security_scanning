def patch_docs(subclass, superclass):
    """
    Apply the documentation from ``superclass`` to ``subclass`` by filling
    in all overridden member function docstrings with those from the
    parent class
    """
    funcs0 = inspect.getmembers(subclass, predicate=inspect.ismethod)
    funcs1 = inspect.getmembers(superclass, predicate=inspect.ismethod)

    funcs1 = [f[0] for f in funcs1]

    for name, func in funcs0:
        if name.startswith('_'):
            continue

        if name not in funcs1:
            continue

        if func.__doc__ is None:
            func = getattr(subclass, name)
            func.__func__.__doc__ = getattr(superclass, name).__func__.__doc__