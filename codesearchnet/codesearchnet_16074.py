def make_into_gene(self):
        '''Tries to make into a gene sequence. Tries all three reading frames and both strands. Returns a tuple (new sequence, strand, frame) if it was successful. Otherwise returns None.'''
        for reverse in [True, False]:
            for frame in range(3):
                new_seq = copy.copy(self)
                if reverse:
                    new_seq.revcomp()
                new_seq.seq = new_seq[frame:]
                if len(new_seq) % 3:
                    new_seq.seq = new_seq.seq[:-(len(new_seq) % 3)]

                new_aa_seq = new_seq.translate()
                if len(new_aa_seq) >= 2 and new_seq[0:3] in genetic_codes.starts[genetic_code] and new_aa_seq[-1] == '*' and '*' not in new_aa_seq[:-1]:
                    strand = '-' if reverse else '+'
                    return new_seq, strand, frame

        return None