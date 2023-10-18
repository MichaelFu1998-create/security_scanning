def drawRoundRect(self, x, y, w, h, r, color=None, aa=False):
        """
        Draw a rounded rectangle with top-left corner at (x, y), width w,
        height h, and corner radius r

        :param aa: if True, use Bresenham's algorithm for line drawing;
            otherwise use Xiaolin Wu's algorithm
        """
        md.draw_round_rect(self.set, x, y, w, h, r, color, aa)