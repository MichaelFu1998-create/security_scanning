def stroke_linejoin(self, linejoin):
        """set to stroke linejoin.

        :param linejoin: 'undefined', 'miter', 'round', 'bevel'
        :type linejoin: str
        """
        linejoin = getattr(pgmagick.LineJoin, "%sJoin" % linejoin.title())
        linejoin = pgmagick.DrawableStrokeLineJoin(linejoin)
        self.drawer.append(linejoin)