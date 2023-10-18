def static(**kwargs):
    """ USE carefully ^^ """
    def wrap(fn):
        fn.func_globals['static'] = fn
        fn.__dict__.update(kwargs)
        return fn
    return wrap