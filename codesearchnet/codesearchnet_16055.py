def contains(self, i):
        '''Returns true iff this interval contains the interval i'''
        return self.start <= i.start and i.end <= self.end