def ellipsemode(self, mode=None):
        '''
        Set the current ellipse drawing mode.

        :param mode: CORNER, CENTER, CORNERS
        :return: ellipsemode if mode is None or valid.
        '''
        if mode in (self.CORNER, self.CENTER, self.CORNERS):
            self.ellipsemode = mode
            return self.ellipsemode
        elif mode is None:
            return self.ellipsemode
        else:
            raise ShoebotError(_("ellipsemode: invalid input"))