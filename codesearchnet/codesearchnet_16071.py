def all_orfs(self, min_length=300):
        '''Finds all open reading frames in the sequence, that are at least as
           long as min_length. Includes ORFs on the reverse strand.
           Returns a list of ORFs, where each element is a tuple:
           (interval.Interval, bool)
           where bool=True means on the reverse strand'''
        orfs = []
        for frame in [0,1,2]:
            for revcomp in [False, True]:
                orfs.extend([(t, revcomp) for t in self.orfs(frame=frame, revcomp=revcomp) if len(t)>=min_length])

        return sorted(orfs, key=lambda t:t[0])