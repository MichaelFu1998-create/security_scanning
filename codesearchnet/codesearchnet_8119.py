def drawLine(self, x0, y0, x1, y1, color=None, colorFunc=None, aa=False):
        """
        Draw a between x0, y0 and x1, y1 in an RGB color.

        :param colorFunc: a function that takes an integer from x0 to x1 and
            returns a color corresponding to that point
        :param aa: if True, use Bresenham's algorithm for line drawing;
            otherwise use Xiaolin Wu's algorithm
        """
        md.draw_line(self.set, x0, y0, x1, y1, color, colorFunc, aa)