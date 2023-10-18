def search(self, search_string):
        '''Finds every occurrence (including overlapping ones) of the search_string, including on the reverse strand. Returns a list where each element is a tuple (position, strand) where strand is in ['-', '+']. Positions are zero-based'''
        seq = self.seq.upper()
        search_string = search_string.upper()
        pos = 0
        found = seq.find(search_string, pos)
        hits = []

        while found != -1:
            hits.append((found, '+'))
            pos = found + 1
            found = seq.find(search_string, pos)


        pos = 0
        search_string = Fasta('x', search_string)
        search_string.revcomp()
        search_string = search_string.seq
        found = seq.find(search_string, pos)

        while found != -1:
            hits.append((found, '-'))
            pos = found + 1
            found = seq.find(search_string, pos)

        return hits