def dropRootPrivs(fn):
    ''' decorator to drop su/sudo privilages before running a function on
        unix/linux.
        The *real* uid is modified, so privileges are permanently dropped for
        the process. (i.e. make sure you don't need to do

        If there is a SUDO_UID environment variable, then we drop to that,
        otherwise we drop to nobody.
    '''

    def wrapped_fn(*args, **kwargs):
        q = multiprocessing.Queue()
        p = multiprocessing.Process(target=_dropPrivsReturnViaQueue, args=(q, fn, args, kwargs))
        p.start()

        r = None
        e = None
        while True:
            msg = q.get()
            if msg[0] == 'return':
                r = msg[1]
            if msg[0] == 'exception':
                e = msg[1](msg[2])
            if msg[0] == 'finish':
                # if the command raised an exception, propagate this:
                if e is not None:
                    raise e #pylint: disable=raising-bad-type
                return r

    return wrapped_fn