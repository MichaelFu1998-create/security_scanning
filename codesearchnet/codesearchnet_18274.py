def acquire_lock(func):
    """Decorate methods when locking repository is required."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        with self.locker as r:
            # get the result
            acquired, code, _  = r
            if acquired:
                try:
                    r = func(self, *args, **kwargs)
                except Exception as err:
                    e = str(err)
                else:
                    e = None
            else:
                warnings.warn("code %s. Unable to aquire the lock when calling '%s'. You may try again!"%(code,func.__name__) )
                e = None
                r = None
        # raise error after exiting with statement and releasing the lock!
        if e is not None:
            traceback.print_stack()
            raise Exception(e)
        return r
    return wrapper