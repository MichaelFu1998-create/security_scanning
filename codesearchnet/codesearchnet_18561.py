def join(prev, sep, *args, **kw):
    '''alias of str.join'''
    yield sep.join(prev, *args, **kw)