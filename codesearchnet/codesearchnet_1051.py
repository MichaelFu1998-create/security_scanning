def sample(self, rgen):
    """Generates a random sample from the Poisson probability distribution and
    returns its value and the log of the probability of sampling that value.
    """
    x = rgen.poisson(self.lambdaParameter)
    return x, self.logDensity(x)