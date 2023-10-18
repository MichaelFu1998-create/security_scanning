def bresenham_line(self, x0, y0, x1, y1, color=None, colorFunc=None):
        """
        Draw line from point x0, y0 to x1, y1 using Bresenham's algorithm.

        Will draw beyond matrix bounds.
        """
        md.bresenham_line(self.set, x0, y0, x1, y1, color, colorFunc)