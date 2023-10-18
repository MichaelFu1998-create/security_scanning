def union(self, i):
        '''If intervals intersect, returns their union, otherwise returns None'''
        if self.intersects(i) or self.end + 1 == i.start or i.end + 1 == self.start:
            return Interval(min(self.start, i.start), max(self.end, i.end))
        else:
            return None