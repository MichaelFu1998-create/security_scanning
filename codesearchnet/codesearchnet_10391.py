def infix_filename(self, name, default, infix, ext=None):
        """Unless *name* is provided, insert *infix* before the extension *ext* of *default*."""
        if name is None:
            p, oldext = os.path.splitext(default)
            if ext is None:
                ext = oldext
            if ext.startswith(os.extsep):
                ext = ext[1:]
            name = self.filename(p+infix, ext=ext)
        return name