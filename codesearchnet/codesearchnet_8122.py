def fillRect(self, x, y, w, h, color=None, aa=False):
        """
        Draw a solid rectangle with top-left corner at (x, y), width w and
        height h.

        :param aa: if True, use Bresenham's algorithm for line drawing;
            otherwise use Xiaolin Wu's algorithm
        """
        md.fill_rect(self.set, x, y, w, h, color, aa)