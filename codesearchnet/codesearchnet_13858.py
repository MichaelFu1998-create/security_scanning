def strokewidth(self, w=None):
        '''Set the stroke width.

        :param w: Stroke width.
        :return: If no width was specified then current width is returned.
        '''
        if w is not None:
            self._canvas.strokewidth = w
        else:
            return self._canvas.strokewidth