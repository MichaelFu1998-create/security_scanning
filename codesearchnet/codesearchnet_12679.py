def with_continuations(**c):
    """
    A decorator for defining tail-call optimized functions.

    Example
    -------

        @with_continuations()
        def factorial(n, k, self=None):
            return self(n-1, k*n) if n > 1 else k
        
        @with_continuations()
        def identity(x, self=None):
            return x
        
        @with_continuations(out=identity)
        def factorial2(n, k, self=None, out=None):
            return self(n-1, k*n) if n > 1 else out(k)

        print(factorial(7,1))
        print(factorial2(7,1))

    """
    if len(c): keys, k = zip(*c.items())
    else: keys, k = tuple([]), tuple([])
    def d(f):
        return C(
            lambda kself, *conts:
                lambda *args:
                    f(*args, self=kself, **dict(zip(keys, conts)))) (*k)
    return d