def directory(cls, directory, root=None, extension=None, **kwargs):
        """
        Load all the files in a given directory selecting only files
        with the given extension if specified. The given kwargs are
        passed through to the normal constructor.
        """
        root = os.getcwd() if root is None else root
        suffix = '' if extension is None else '.' + extension.rsplit('.')[-1]
        pattern = directory + os.sep + '*' + suffix
        key = os.path.join(root, directory,'*').rsplit(os.sep)[-2]
        format_parse = list(string.Formatter().parse(key))
        if not all([el is None for el in zip(*format_parse)[1]]):
            raise Exception('Directory cannot contain format field specifications')
        return cls(key, pattern, root, **kwargs)