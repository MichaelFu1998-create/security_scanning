def stopper(func):
        """Wrap a conditoinal function(stopper function) to Pipe object.

        wrapped function should return boolean value. The cascading pipe will
        stop the execution if wrapped function return True.

        Stopper is useful if you have unlimited number of input data.

        :param func: The conditoinal function to be wrapped.
        :type func: function object
        :param args: The default arguments to be used for wrapped function.
        :param kw:  The default keyword arguments to be used for wrapped function.
        :returns: Pipe object
        """
        def wrapper(prev, *argv, **kw):
            if prev is None:
                raise TypeError('A stopper must have input.')
            for i in prev:
                if func(i, *argv, **kw):
                    break
                yield i
        return Pipe(wrapper)