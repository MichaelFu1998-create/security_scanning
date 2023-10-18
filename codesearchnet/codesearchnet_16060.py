def subseq(self, start, end):
        '''Returns Fasta object with the same name, of the bases from start to end, but not including end'''
        return Fasta(self.id, self.seq[start:end])