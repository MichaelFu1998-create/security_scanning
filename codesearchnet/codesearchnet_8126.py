def drawTriangle(self, x0, y0, x1, y1, x2, y2, color=None, aa=False):
        """
        Draw triangle with vertices (x0, y0), (x1, y1) and (x2, y2)

        :param aa: if True, use Bresenham's algorithm for line drawing;
            Otherwise use Xiaolin Wu's algorithm
        """
        md.draw_triangle(self.set, x0, y0, x1, y1, x2, y2, color, aa)