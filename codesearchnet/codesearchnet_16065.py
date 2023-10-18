def add_insertions(self, skip=10, window=1, test=False):
        '''Adds a random base within window bases around every skip bases. e.g. skip=10, window=1 means a random base added somwhere in theintervals [9,11], [19,21] ... '''
        assert 2 * window < skip
        new_seq = list(self.seq)
        for i in range(len(self) - skip, 0, -skip):
            pos = random.randrange(i - window, i + window + 1)
            base = random.choice(['A', 'C', 'G', 'T'])
            if test:
                base = 'N'
            new_seq.insert(pos, base)

        self.seq = ''.join(new_seq)