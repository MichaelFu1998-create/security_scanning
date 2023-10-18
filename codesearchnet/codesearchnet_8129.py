def drawText(self, text, x=0, y=0, color=None,
                 bg=colors.COLORS.Off, aa=False, font=font.default_font,
                 font_scale=1):
        """
        Draw a line of text starting at (x, y) in an RGB color.

        :param colorFunc: a function that takes an integer from x0 to x1 and
            returns a color corresponding to that point
        :param aa: if True, use Bresenham's algorithm for line drawing;
            otherwise use Xiaolin Wu's algorithm
        """
        md.draw_text(self.fonts, self.set, text, self.width, self.height,
                     x, y, color, bg, aa, font, font_scale)