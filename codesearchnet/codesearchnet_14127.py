def _curvelength(self, x0, y0, x1, y1, x2, y2, x3, y3, n=20):
        """ Returns the length of the spline.
            Integrates the estimated length of the cubic bezier spline defined by x0, y0, ... x3, y3,
            by adding the lengths of lineair lines between points at t.
            The number of points is defined by n
            (n=10 would add the lengths of lines between 0.0 and 0.1, between 0.1 and 0.2, and so on).
            The default n=20 is fine for most cases, usually resulting in a deviation of less than 0.01.
        """
        # Originally from nodebox-gl
        length = 0
        xi = x0
        yi = y0
        for i in range(n):
            t = 1.0 * (i + 1) / n
            pt_x, pt_y, pt_c1x, pt_c1y, pt_c2x, pt_c2y = \
                self._curvepoint(t, x0, y0, x1, y1, x2, y2, x3, y3)
            c = sqrt(pow(abs(xi - pt_x), 2) + pow(abs(yi - pt_y), 2))
            length += c
            xi = pt_x
            yi = pt_y
        return length