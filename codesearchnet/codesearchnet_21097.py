def load(cls, fh):
        """
        Load json or yaml data from file handle.

        Args:
            fh (file): File handle to load from.

        Examlple:
            >>> with open('data.json', 'r') as json:
            >>>    jsdata = composite.load(json)
            >>>
            >>> with open('data.yml', 'r') as yml:
            >>>    ymldata = composite.load(yml)
        """
        dat = fh.read()
        try:
            ret = cls.from_json(dat)
        except:
            ret = cls.from_yaml(dat)
        return ret