def orfs(self, frame=0, revcomp=False):
        '''Returns a list of ORFs that the sequence has, starting on the given
           frame. Each returned ORF is an interval.Interval object.
           If revomp=True, then finds the ORFs of the reverse complement
           of the sequence.'''
        assert frame in [0,1,2]
        if revcomp:
            self.revcomp()

        aa_seq = self.translate(frame=frame).seq.rstrip('X')
        if revcomp:
            self.revcomp()

        orfs = _orfs_from_aa_seq(aa_seq)
        for i in range(len(orfs)):
            if revcomp:
                start = len(self) - (orfs[i].end * 3 + 3) - frame
                end = len(self) - (orfs[i].start * 3) - 1 - frame
            else:
                start = orfs[i].start * 3 + frame
                end = orfs[i].end * 3 + 2 + frame

            orfs[i] = intervals.Interval(start, end)

        return orfs