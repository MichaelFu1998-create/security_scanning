def size(self, w=None, h=None):
        '''Set the canvas size

        Only the first call will actually be effective.

        :param w: Width
        :param h: height
        '''

        if not w:
            w = self._canvas.width
        if not h:
            h = self._canvas.height
        if not w and not h:
            return (self._canvas.width, self._canvas.height)

        # FIXME: Updating in all these places seems a bit hacky
        w, h = self._canvas.set_size((w, h))
        self._namespace['WIDTH'] = w
        self._namespace['HEIGHT'] = h
        self.WIDTH = w  # Added to make evolution example work
        self.HEIGHT = h