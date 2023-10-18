def _calculate(self):
        self.logpriors = np.zeros_like(self.rad)

        for i in range(self.N-1):
            o = np.arange(i+1, self.N)

            dist = ((self.zscale*(self.pos[i] - self.pos[o]))**2).sum(axis=-1)
            dist0 = (self.rad[i] + self.rad[o])**2

            update = self.prior_func(dist - dist0)
            self.logpriors[i] += np.sum(update)
            self.logpriors[o] += update

        """
        # This is equivalent
        for i in range(self.N-1):
            for j in range(i+1, self.N):
                d = ((self.zscale*(self.pos[i] - self.pos[j]))**2).sum(axis=-1)
                r = (self.rad[i] + self.rad[j])**2

                cost = self.prior_func(d - r)
                self.logpriors[i] += cost
                self.logpriors[j] += cost
        """