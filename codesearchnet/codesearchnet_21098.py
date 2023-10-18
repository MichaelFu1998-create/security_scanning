def from_json(cls, fh):
        """
        Load json from file handle.

        Args:
            fh (file): File handle to load from.

        Examlple:
            >>> with open('data.json', 'r') as json:
            >>>    data = composite.load(json)
        """
        if isinstance(fh, str):
            return cls(json.loads(fh))
        else:
            return cls(json.load(fh))