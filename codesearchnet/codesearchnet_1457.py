def propose(self, current, r):
    """Generates a random sample from the discrete probability distribution and
    returns its value, the log of the probability of sampling that value and the
    log of the probability of sampling the current value (passed in).
    """
    stay = (r.uniform(0, 1) < self.kernel)
    if stay:
      logKernel = numpy.log(self.kernel)
      return current, logKernel, logKernel
    else: # Choose uniformly, not according to the pmf.
      curIndex = self.keyMap[current]
      ri = r.randint(0, self.nKeys-1)
      logKernel = numpy.log(1.0 - self.kernel)
      lp = logKernel + self.logp
      if ri < curIndex: return self.keys[ri], lp, lp
      else: return self.keys[ri+1], lp, lp