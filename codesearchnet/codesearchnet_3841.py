def encoding(self):
        """
        Gets the encoding of the `redirect` IO object

        Doctest:
            >>> redirect = io.StringIO()
            >>> assert TeeStringIO(redirect).encoding is None
            >>> assert TeeStringIO(None).encoding is None
            >>> assert TeeStringIO(sys.stdout).encoding is sys.stdout.encoding
            >>> redirect = io.TextIOWrapper(io.StringIO())
            >>> assert TeeStringIO(redirect).encoding is redirect.encoding
        """
        if self.redirect is not None:
            return self.redirect.encoding
        else:
            return super(TeeStringIO, self).encoding