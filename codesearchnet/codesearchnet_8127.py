def fillTriangle(self, x0, y0, x1, y1, x2, y2, color=None, aa=False):
        """
        Draw filled triangle with points x0,y0 - x1,y1 - x2,y2

        :param aa: if True, use Bresenham's algorithm for line drawing;
            otherwise use Xiaolin Wu's algorithm
        """
        md.fill_triangle(self.set, x0, y0, x1, y1, x2, y2, color, aa)