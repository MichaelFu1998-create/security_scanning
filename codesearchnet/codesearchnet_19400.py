def score(self, plaintext):
        "Return a score for text based on how common letters pairs are."
        s = 1.0
        for bi in bigrams(plaintext):
            s = s * self.P2[bi]
        return s