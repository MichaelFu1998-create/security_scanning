def translate(self, frame=0):
        '''Returns a Fasta sequence, translated into amino acids. Starts translating from 'frame', where frame expected to be 0,1 or 2'''
        return Fasta(self.id, ''.join([genetic_codes.codes[genetic_code].get(self.seq[x:x+3].upper(), 'X') for x in range(frame, len(self)-1-frame, 3)]))