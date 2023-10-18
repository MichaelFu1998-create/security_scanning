def intersects(self, b):
        """ Return True if a part of the two bounds overlaps.
        """
        return max(self.x, b.x) < min(self.x+self.width, b.x+b.width) \
           and max(self.y, b.y) < min(self.y+self.height, b.y+b.height)