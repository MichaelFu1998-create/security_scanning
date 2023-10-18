def sample(self):
        "Return a random sample from the distribution."
        if self.sampler is None:
            self.sampler = weighted_sampler(self.dictionary.keys(),
                                            self.dictionary.values())
        return self.sampler()