def _newRep(self):
    """Generate a new and unique representation. Returns a numpy array
    of shape (n,). """
    maxAttempts = 1000

    for _ in xrange(maxAttempts):
      foundUnique = True
      population = numpy.arange(self.n, dtype=numpy.uint32)
      choices = numpy.arange(self.w, dtype=numpy.uint32)
      oneBits = sorted(self.random.sample(population, choices))
      sdr =  numpy.zeros(self.n, dtype='uint8')
      sdr[oneBits] = 1
      for i in xrange(self.ncategories):
        if (sdr == self.sdrs[i]).all():
          foundUnique = False
          break
      if foundUnique:
        break;
    if not foundUnique:
      raise RuntimeError("Error, could not find unique pattern %d after "
                         "%d attempts" % (self.ncategories, maxAttempts))
    return sdr