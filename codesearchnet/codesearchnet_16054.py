def intersects(self, i):
        '''Returns true iff this interval intersects the interval i'''
        return self.start <= i.end and i.start <= self.end