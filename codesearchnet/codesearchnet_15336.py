def scaling(self, x, y):
        """Scaling Draw Object

        :param x: 0.0 ~ 1.0
        :param y: 0.0 ~ 1.0
        """
        self.drawer.append(pgmagick.DrawableScaling(float(x), float(y)))