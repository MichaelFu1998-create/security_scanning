def flush(self):  # nocover
        """
        Flush to this and the redirected stream
        """
        if self.redirect is not None:
            self.redirect.flush()
        super(TeeStringIO, self).flush()