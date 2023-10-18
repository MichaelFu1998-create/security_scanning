def default(fun, **kwdefault):
    """
    change default value for function
    ex)
    def sample(a, b=1, c=1):
        print 'from sample:', a, b, c
        return a, b, c
    fun = default(sample, b=4,c=5)
    print fun.default  # get default value dictionary
    fun(1)  # print 1, 5, 5 and return

    :param fun:
    :param kwdefault:
    :return:
    """

    @functools.wraps(fun)
    def wrapped(*args, **kwargs):
        merge = wrapped.default.copy()
        merge.update(kwargs)
        return fun(*args, **merge)

    wrapped.default = kwdefault

    return wrapped