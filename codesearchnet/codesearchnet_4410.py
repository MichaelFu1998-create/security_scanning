def async_process(fn):
    """ Decorator function to launch a function as a separate process """

    def run(*args, **kwargs):
        proc = mp.Process(target=fn, args=args, kwargs=kwargs)
        proc.start()
        return proc

    return run