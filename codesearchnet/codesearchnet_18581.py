def reduce(func):
        """Wrap a reduce function to Pipe object. Reduce function is a function
        with at least two arguments. It works like built-in reduce function.
        It takes first argument for accumulated result, second argument for
        the new data to process. A keyword-based argument named 'init' is
        optional. If init is provided, it is used for the initial value of
        accumulated result. Or, the initial value is None.

        The first argument is the data to be converted. The return data from
        filter function should be a boolean value. If true, data can pass.
        Otherwise, data is omitted.

        :param func: The filter function to be wrapped.
        :type func: function object
        :param args: The default arguments to be used for filter function.
        :param kw: The default keyword arguments to be used for filter function.
        :returns: Pipe object
        """
        def wrapper(prev, *argv, **kw):
            accum_value = None if 'init' not in kw else kw.pop('init')
            if prev is None:
                raise TypeError('A reducer must have input.')
            for i in prev:
                accum_value = func(accum_value, i, *argv, **kw)
            yield accum_value
        return Pipe(wrapper)