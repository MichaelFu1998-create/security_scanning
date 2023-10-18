def transform(self, mode=None):
        '''
        Set the current transform mode.

        :param mode: CENTER or CORNER'''
        if mode:
            self._canvas.mode = mode
        return self._canvas.mode