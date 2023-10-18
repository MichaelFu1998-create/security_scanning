def union(self, b):
        """ Returns bounds that encompass the union of the two.
        """
        mx, my = min(self.x, b.x), min(self.y, b.y)
        return Bounds(mx, my,
            max(self.x+self.width, b.x+b.width) - mx,
            max(self.y+self.height, b.y+b.height) - my)