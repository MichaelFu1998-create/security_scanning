def setup_once(initfn):
    """
    call class instance method for initial setup ::

        class B(object):

            def init(self, a):
                print 'init call:', a

            @setup_once(init)
            def mycall(self, a):
                print 'real call:', a

        b = B()
        b.mycall(222)
        b.mycall(333)

    :param function initfn:
    :return: decorated method
    """
    def wrap(method):

        finit = initfn.__name__
        fnname = method.__name__

        @functools.wraps(method)
        def wrapped(self, *args, **kwargs):

            @functools.wraps(method)
            def aftersetup(*a, **kw):
                return method(self, *a, **kw)

            setupfn = getattr(self, finit)
            setupfn(*args, **kwargs)

            res = method(self, *args, **kwargs)
            setattr(self, fnname, aftersetup)
            return res
        return wrapped

    return wrap