def labels(self):
        '''Return the names of our marker labels in canonical order.'''
        return sorted(self.channels, key=lambda c: self.channels[c])