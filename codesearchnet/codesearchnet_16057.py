def union_fill_gap(self, i):
        '''Like union, but ignores whether the two intervals intersect or not'''
        return Interval(min(self.start, i.start), max(self.end, i.end))