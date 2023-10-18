def drawChar(self, x, y, c, color, bg,
                 aa=False, font=font.default_font, font_scale=1):
        """
        Draw a single character c at at (x, y) in an RGB color.
        """
        md.draw_char(self.fonts, self.set, self.width, self.height,
                     x, y, c, color, bg, aa, font, font_scale)