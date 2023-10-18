def stroke_linecap(self, linecap):
        """set to stroke linecap.

        :param linecap: 'undefined', 'butt', 'round', 'square'
        :type linecap: str
        """
        linecap = getattr(pgmagick.LineCap, "%sCap" % linecap.title())
        linecap = pgmagick.DrawableStrokeLineCap(linecap)
        self.drawer.append(linecap)