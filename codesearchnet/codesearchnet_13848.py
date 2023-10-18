def relmoveto(self, x, y):
        '''Move relatively to the last point.'''
        if self._path is None:
            raise ShoebotError(_("No current path. Use beginpath() first."))
        self._path.relmoveto(x, y)