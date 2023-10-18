def predictor(self, (i, j, A, alpha, Bb)):
        "Add to chart any rules for B that could help extend this edge."
        B = Bb[0]
        if B in self.grammar.rules:
            for rhs in self.grammar.rewrites_for(B):
                self.add_edge([j, j, B, [], rhs])