def apply_function(self, points):
        """Run the filter function on the provided points."""
        if not self.option.function:
            return points

        if np is None:
            raise ImportError('numpy is not available')

        if ':' in self.option.function:
            function, arguments = self.option.function.split(':', 1)
            arguments = arguments.split(',')
        else:
            function = self.option.function
            arguments = []

        # Resolve arguments
        arguments = list(map(self._function_argument, arguments))

        # Resolve function
        filter_function = FUNCTION.get(function)

        if filter_function is None:
            raise TypeError('Invalid function "%s"' % (function,))

        else:
            # We wrap in ``list()`` to consume generators and iterators, as
            # ``np.array`` doesn't do this for us.
            return filter_function(np.array(list(points)), *arguments)