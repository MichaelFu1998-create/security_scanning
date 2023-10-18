def expand_nucleotides(self):
        '''Assumes sequence is nucleotides. Returns list of all combinations of redundant nucleotides. e.g. R is A or G, so CRT would have combinations CAT and CGT'''
        s = list(self.seq)
        for i in range(len(s)):
            if s[i] in redundant_nts:
                s[i] = ''.join(redundant_nts[s[i]])

        seqs = []
        for x in itertools.product(*s):
            seqs.append(Fasta(self.id + '.' + str(len(seqs) + 1), ''.join(x)))
        return seqs