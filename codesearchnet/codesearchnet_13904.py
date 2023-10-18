def intersection(self, b):
        """ Returns bounds that encompass the intersection of the two.
            If there is no overlap between the two, None is returned.
        """
        if not self.intersects(b):
            return None
        mx, my = max(self.x, b.x), max(self.y, b.y)
        return Bounds(mx, my,
            min(self.x+self.width, b.x+b.width) - mx,
            min(self.y+self.height, b.y+b.height) - my)