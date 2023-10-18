def translate(self, xt, yt, mode=None):
        '''
        Translate the current position by (xt, yt) and
        optionally set the transform mode.

        :param xt: Amount to move horizontally
        :param yt: Amount to move vertically
        :mode: Set the transform mode to CENTER or CORNER
        '''
        self._canvas.translate(xt, yt)
        if mode:
            self._canvas.mode = mode