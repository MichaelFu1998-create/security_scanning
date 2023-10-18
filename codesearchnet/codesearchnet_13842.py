def rectmode(self, mode=None):
        '''
        Set the current rectmode.

        :param mode: CORNER, CENTER, CORNERS
        :return: rectmode if mode is None or valid.
        '''
        if mode in (self.CORNER, self.CENTER, self.CORNERS):
            self.rectmode = mode
            return self.rectmode
        elif mode is None:
            return self.rectmode
        else:
            raise ShoebotError(_("rectmode: invalid input"))