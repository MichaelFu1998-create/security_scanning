def looks_like_gene(self):
        '''Returns true iff: length >=6, length is a multiple of 3, first codon is start, last codon is a stop and has no other stop codons'''
        return self.is_complete_orf() \
          and len(self) >= 6 \
          and len(self) %3 == 0 \
          and self.seq[0:3].upper() in genetic_codes.starts[genetic_code]