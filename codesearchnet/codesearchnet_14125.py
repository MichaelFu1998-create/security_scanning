def _linelength(self, x0, y0, x1, y1):
        """ Returns the length of the line.
        """
        # Originally from nodebox-gl
        a = pow(abs(x0 - x1), 2)
        b = pow(abs(y0 - y1), 2)
        return sqrt(a + b)