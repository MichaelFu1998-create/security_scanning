def bindargs(fun, *argsbind, **kwbind):
    """
    _ = bind.placeholder   # unbound placeholder (arg)
    f = bind(fun, _, _, arg3, kw=kw1, kw2=kw2), f(arg1, arg2)
    :param fun:
    :param argsbind:
    :param kwbind:
    :return:
    """

    assert argsbind
    argsb = list(argsbind)
    iargs = [i for i in range(len(argsbind)) if argsbind[i] is bind.placeholder]
    # iargs = [a is bind.placeholder for a in argsbind]

    @functools.wraps(fun)
    def wrapped(*args, **kwargs):
        kws = kwbind.copy()

        args_this = [a for a in argsb]
        for i, arg in zip(iargs, args):
            args_this[i] = arg
        args_this.extend(args[len(iargs):])

        # kwargs.update(kwbind)
        kws.update(kwargs)
        # return fun(*argsb, **kws)
        return fun(*args_this, **kws)

    return wrapped