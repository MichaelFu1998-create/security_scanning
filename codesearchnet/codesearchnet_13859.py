def font(self, fontpath=None, fontsize=None):
        '''Set the font to be used with new text instances.

        :param fontpath: path to truetype or opentype font.
        :param fontsize: size of font

        :return: current current fontpath (if fontpath param not set)
        Accepts TrueType and OpenType files. Depends on FreeType being
        installed.'''
        if fontpath is not None:
            self._canvas.fontfile = fontpath
        else:
            return self._canvas.fontfile
        if fontsize is not None:
            self._canvas.fontsize = fontsize