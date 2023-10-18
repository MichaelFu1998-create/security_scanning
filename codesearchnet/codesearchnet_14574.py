def _b(s, encoding='utf-8'):
        """
        Returns the given string as a string of bytes. That means in
        Python2 as a str object, and in Python3 as a bytes object.
        Raises a TypeError, if it cannot be converted.
        """
        if six.PY2:
            # This is Python2
            if isinstance(s, str):
                return s
            elif isinstance(s, unicode):  # noqa, pylint: disable=undefined-variable
                return s.encode(encoding)
        else:
            # And this is Python3
            if isinstance(s, bytes):
                return s
            elif isinstance(s, str):
                return s.encode(encoding)

        raise TypeError("Invalid argument %r for _b()" % (s,))