def score(self, code):
        """Score is product of word scores, unigram scores, and bigram scores.
        This can get very small, so we use logs and exp."""
        text = permutation_decode(self.ciphertext, code)
        logP = (sum([log(self.Pwords[word]) for word in words(text)]) +
                sum([log(self.P1[c]) for c in text]) +
                sum([log(self.P2[b]) for b in bigrams(text)]))
        return exp(logP)