def stroke_antialias(self, flag=True):
        """stroke antialias

        :param flag: True or False. (default is True)
        :type flag: bool
        """
        antialias = pgmagick.DrawableStrokeAntialias(flag)
        self.drawer.append(antialias)