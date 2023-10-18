def pathjoin(*args, **kwargs):
    """
    Arguments:
        args (list): *args list of paths
            if len(args) == 1, args[0] is not a string, and args[0] is iterable,
            set args to args[0].

    Basically::

        joined_path = u'/'.join(
            [args[0].rstrip('/')] +
            [a.strip('/') for a in args[1:-1]] +
            [args[-1].lstrip('/')])
    """
    log.debug('pathjoin: %r' % list(args))

    def _pathjoin(*args, **kwargs):
        len_ = len(args) - 1
        if len_ < 0:
            raise Exception('no args specified')
        elif len_ == 0:
            if not isinstance(args, basestring):
                if hasattr(args, '__iter__'):
                    _args = args
                    _args
                    args = args[0]
        for i, arg in enumerate(args):
            if not i:
                yield arg.rstrip('/')
            elif i == len_:
                yield arg.lstrip('/')
            else:
                yield arg.strip('/')
    joined_path = u'/'.join(_pathjoin(*args))
    return sanitize_path(joined_path)