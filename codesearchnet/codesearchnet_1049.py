def sample(self, rgen):
    """Generates a random sample from the discrete probability distribution
    and returns its value and the log of the probability of sampling that value.
    """
    rf = rgen.uniform(0, self.sum)
    index = bisect.bisect(self.cdf, rf)
    return self.keys[index], numpy.log(self.pmf[index])