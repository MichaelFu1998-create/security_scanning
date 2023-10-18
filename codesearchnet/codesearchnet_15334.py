def fill_opacity(self, opacity):
        """
        :param opacity: 0.0 ~ 1.0
        """
        opacity = pgmagick.DrawableFillOpacity(float(opacity))
        self.drawer.append(opacity)