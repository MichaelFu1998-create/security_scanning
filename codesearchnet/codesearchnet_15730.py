def read(self, n):
        """ return at most n array items, move the cursor. 
        """
        while len(self.pool) < n:
            self.cur = self.files.next()
            self.pool = numpy.append(self.pool,
                    self.fetch(self.cur), axis=0)

        rt = self.pool[:n]
        if n == len(self.pool):
            self.pool = self.fetch(None)
        else:
            self.pool = self.pool[n:]
        return rt