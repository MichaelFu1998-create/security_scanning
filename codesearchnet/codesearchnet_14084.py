def blend(self, clr, factor=0.5):
        """
        Returns a mix of two colors.
        """
        r = self.r * (1 - factor) + clr.r * factor
        g = self.g * (1 - factor) + clr.g * factor
        b = self.b * (1 - factor) + clr.b * factor
        a = self.a * (1 - factor) + clr.a * factor
        return Color(r, g, b, a, mode="rgb")