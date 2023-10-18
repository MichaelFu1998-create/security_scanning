def distance_to_point(self, p):
        '''Returns the distance from the point to the interval. Zero if the point lies inside the interval.'''
        if self.start <= p <= self.end:
            return 0
        else:
            return min(abs(self.start - p), abs(self.end - p))