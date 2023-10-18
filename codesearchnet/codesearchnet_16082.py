def trim_Ns(self):
        '''Removes any leading or trailing N or n characters from the sequence'''
        # get index of first base that is not an N
        i = 0
        while i < len(self) and self.seq[i] in 'nN':
            i += 1

        # strip off start of sequence and quality
        self.seq = self.seq[i:]
        self.qual = self.qual[i:]

        # strip the ends
        self.seq = self.seq.rstrip('Nn')
        self.qual = self.qual[:len(self.seq)]