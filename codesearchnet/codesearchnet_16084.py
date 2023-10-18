def translate(self):
        '''Returns a Fasta sequence, translated into amino acids. Starts translating from 'frame', where frame expected to be 0,1 or 2'''
        fa = super().translate()
        return Fastq(fa.id, fa.seq, 'I'*len(fa.seq))