def samples(self, nwords):
        """Build up a random sample of text nwords words long, using
        the conditional probability given the n-1 preceding words."""
        n = self.n
        nminus1gram = ('',) * (n-1)
        output = []
        for i in range(nwords):
            if nminus1gram not in self.cond_prob:
                nminus1gram = ('',) * (n-1) # Cannot continue, so restart.
            wn = self.cond_prob[nminus1gram].sample()
            output.append(wn)
            nminus1gram = nminus1gram[1:] + (wn,)
        return ' '.join(output)