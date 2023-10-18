def print(self, *objects, **options):
        """
        Print the given objects to the given file stream.
        See https://docs.python.org/3/library/functions.html#print

        The only difference to the ``print()`` built-in is that
        ``Colorful.print()`` formats the string with ``c=self``.
        With that stylings are possible

        :param str sep: the seperater between the objects
        :param str end: the ending delimiter after all objects
        :param file: the file stream to write to
        :param bool flush: if the stream should be flushed
        """
        # NOTE: change signature to same as print() built-in function as
        #       soon as Python 2.7 is not supported anymore.
        #       If causes problems because of the keyword args after *args
        allowed_options = {'sep', 'end', 'file', 'flush'}
        given_options = set(options.keys())
        if not given_options.issubset(allowed_options):
            raise TypeError('Colorful.print() got unexpected keyword arguments: {0}'.format(
                ', '.join(given_options.difference(allowed_options))))

        sep = options.get('sep', ' ')
        end = options.get('end', '\n')
        file = options.get('file', sys.stdout)
        flush = options.get('flush', False)

        styled_objects = [self.format(o) for o in objects]
        print(*styled_objects, sep=sep, end=end, file=file)

        # NOTE: if Python 2.7 support is dropped we can directly forward the
        #       flush keyword argument to the print() function.
        if flush:
            file.flush()