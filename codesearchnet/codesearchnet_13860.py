def fontsize(self, fontsize=None):
        '''
        Set or return size of current font.

        :param fontsize: Size of font.
        :return: Size of font (if fontsize was not specified)
        '''
        if fontsize is not None:
            self._canvas.fontsize = fontsize
        else:
            return self._canvas.fontsize