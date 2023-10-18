def logProbability(self, distn):
    """Form of distribution must be an array of counts in order of self.keys."""
    x = numpy.asarray(distn)
    n = x.sum()
    return (logFactorial(n) - numpy.sum([logFactorial(k) for k in x]) +
      numpy.sum(x * numpy.log(self.dist.pmf)))