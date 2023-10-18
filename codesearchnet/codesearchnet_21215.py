def keep_kwargs_partial(func, *args, **keywords):
    """Like functools.partial but instead of using the new kwargs, keeps the old ones."""
    def newfunc(*fargs, **fkeywords):
        newkeywords = fkeywords.copy()
        newkeywords.update(keywords)
        return func(*(args + fargs), **newkeywords)
    newfunc.func = func
    newfunc.args = args
    newfunc.keywords = keywords
    return newfunc