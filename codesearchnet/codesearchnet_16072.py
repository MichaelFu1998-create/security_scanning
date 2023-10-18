def is_complete_orf(self):
        '''Returns true iff length is >= 6, is a multiple of 3, and there is exactly one stop codon in the sequence and it is at the end'''
        if len(self) %3 != 0 or len(self) < 6:
            return False

        orfs = self.orfs()
        complete_orf = intervals.Interval(0, len(self) - 1)
        for orf in orfs:
            if orf == complete_orf:
                return True
        return False