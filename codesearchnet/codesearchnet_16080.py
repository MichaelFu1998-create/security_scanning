def subseq(self, start, end):
        '''Returns Fastq object with the same name, of the bases from start to end, but not including end'''
        return Fastq(self.id, self.seq[start:end], self.qual[start:end])