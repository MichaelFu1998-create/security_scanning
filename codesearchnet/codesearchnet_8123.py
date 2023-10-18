def fillScreen(self, color=None):
        """Fill the matrix with the given RGB color"""
        md.fill_rect(self.set, 0, 0, self.width, self.height, color)