def format(self, string, *args, **kwargs):
        """
        Format the given string with the given ``args`` and ``kwargs``.
        The string can contain references to ``c`` which is provided by
        this colorful object.

        :param str string: the string to format
        """
        return string.format(c=self, *args, **kwargs)