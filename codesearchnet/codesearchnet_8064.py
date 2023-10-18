def _get_param_names(cls):
        '''Get the list of parameter names for the object'''

        init = cls.__init__

        args, varargs = inspect.getargspec(init)[:2]

        if varargs is not None:
            raise RuntimeError('BaseTransformer objects cannot have varargs')

        args.pop(0)
        args.sort()
        return args