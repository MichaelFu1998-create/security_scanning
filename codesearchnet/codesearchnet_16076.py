def to_Fastq(self, qual_scores):
        '''Returns a Fastq object. qual_scores expected to be a list of numbers, like you would get in a .qual file'''
        if len(self) != len(qual_scores):
            raise Error('Error making Fastq from Fasta, lengths differ.', self.id)
        return Fastq(self.id, self.seq, ''.join([chr(max(0, min(x, 93)) + 33) for x in qual_scores]))