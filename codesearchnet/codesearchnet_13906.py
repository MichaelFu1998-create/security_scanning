def contains(self, *a):
        """ Returns True if the given point or rectangle falls within the bounds.
        """
        if len(a) == 2: a = [Point(a[0], a[1])]
        if len(a) == 1:
            a = a[0]
            if isinstance(a, Point):
                return a.x >= self.x and a.x <= self.x+self.width \
                   and a.y >= self.y and a.y <= self.y+self.height
            if isinstance(a, Bounds):
                return a.x >= self.x and a.x+a.width <= self.x+self.width \
                   and a.y >= self.y and a.y+a.height <= self.y+self.height