def try_delegation(method):
    '''This decorator wraps descriptor methods with a new method that tries
    to delegate to a function of the same name defined on the owner instance
    for convenience for dispatcher clients.
    '''
    @functools.wraps(method)
    def delegator(self, *args, **kwargs):
        if self.try_delegation:
            # Try to dispatch to the instance's implementation.
            inst = getattr(self, 'inst', None)
            if inst is not None:
                method_name = (self.delegator_prefix or '') + method.__name__
                func = getattr(inst, method_name, None)
                if func is not None:
                    return func(*args, **kwargs)

        # Otherwise run the decorated func.
        return method(self, *args, **kwargs)

    return delegator