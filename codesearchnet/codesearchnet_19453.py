def score(self):
        "The total score for the words found, according to the rules."
        return sum([self.scores[len(w)] for w in self.words()])