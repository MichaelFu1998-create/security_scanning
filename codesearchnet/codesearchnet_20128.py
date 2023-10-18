def _make_dispatch(cls, func):
        '''
        Create a dispatch pair for func- a tuple of (bind_args, func), where
        bind_args is a function that, when called with (args, kwargs), attempts
        to bind those args to the type signature of func, or else raise a
        TypeError
        '''
        sig = signature(func)
        matchers = tuple(cls._make_all_matchers(sig.parameters.items()))
        return (partial(cls._bind_args, sig, matchers), func)