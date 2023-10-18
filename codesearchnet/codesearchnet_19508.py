def normalize(self):
        "Return my probabilities; must be down to one variable."
        assert len(self.vars) == 1
        return ProbDist(self.vars[0],
                        dict((k, v) for ((k,), v) in self.cpt.items()))