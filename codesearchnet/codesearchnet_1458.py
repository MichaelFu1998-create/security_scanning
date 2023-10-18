def propose(self, current, r):
    """Generates a random sample from the Poisson probability distribution with
    with location and scale parameter equal to the current value (passed in).
    Returns the value of the random sample, the log of the probability of
    sampling that value, and the log of the probability of sampling the current
    value if the roles of the new sample and the current sample were reversed
    (the log of the backward proposal probability).
    """
    curLambda = current + self.offset
    x, logProb = PoissonDistribution(curLambda).sample(r)
    logBackward = PoissonDistribution(x+self.offset).logDensity(current)
    return x, logProb, logBackward