def rellineto(self, x, y):
        '''Draw a line using relative coordinates.'''
        if self._path is None:
            raise ShoebotError(_("No current path. Use beginpath() first."))
        self._path.rellineto(x, y)