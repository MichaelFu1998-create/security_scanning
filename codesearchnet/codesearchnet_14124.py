def _linepoint(self, t, x0, y0, x1, y1):
        """ Returns coordinates for point at t on the line.
            Calculates the coordinates of x and y for a point at t on a straight line.
            The t parameter is a number between 0.0 and 1.0,
            x0 and y0 define the starting point of the line,
            x1 and y1 the ending point of the line.
        """
        # Originally from nodebox-gl
        out_x = x0 + t * (x1 - x0)
        out_y = y0 + t * (y1 - y0)
        return (out_x, out_y)