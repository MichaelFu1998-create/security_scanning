def relcurveto(self, h1x, h1y, h2x, h2y, x, y):
        '''Draws a curve relatively to the last point.
        '''
        if self._path is None:
            raise ShoebotError(_("No current path. Use beginpath() first."))
        self._path.relcurveto(h1x, h1y, h2x, h2y, x, y)