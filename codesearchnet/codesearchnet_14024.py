def size_or_default(self):
        '''
        If size is not set, otherwise set size to DEFAULT_SIZE
        and return it.

        This means, only the first call to size() is valid.
        '''
        if not self.size:
            self.size = self.DEFAULT_SIZE
        return self.size