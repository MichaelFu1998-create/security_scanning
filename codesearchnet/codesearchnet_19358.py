def smooth_for(self, o):
        """Include o among the possible observations, whether or not
        it's been observed yet."""
        if o not in self.dictionary:
            self.dictionary[o] = self.default
            self.n_obs += self.default
            self.sampler = None