def add(self, o):
        "Add an observation o to the distribution."
        self.smooth_for(o)
        self.dictionary[o] += 1
        self.n_obs += 1
        self.sampler = None