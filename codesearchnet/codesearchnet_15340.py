def text_antialias(self, flag=True):
        """text antialias

        :param flag: True or False. (default is True)
        :type flag: bool
        """
        antialias = pgmagick.DrawableTextAntialias(flag)
        self.drawer.append(antialias)