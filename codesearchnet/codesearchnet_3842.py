def write(self, msg):
        """
        Write to this and the redirected stream
        """
        if self.redirect is not None:
            self.redirect.write(msg)
        if six.PY2:
            from xdoctest.utils.util_str import ensure_unicode
            msg = ensure_unicode(msg)
        super(TeeStringIO, self).write(msg)