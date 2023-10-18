def intersection(self, i):
        '''If intervals intersect, returns their intersection, otherwise returns None'''
        if self.intersects(i):
            return Interval(max(self.start, i.start), min(self.end, i.end))
        else:
            return None