def nostroke(self):
        ''' Stop applying strokes to new paths.

        :return: stroke color before nostroke was called.
        '''
        c = self._canvas.strokecolor
        self._canvas.strokecolor = None
        return c