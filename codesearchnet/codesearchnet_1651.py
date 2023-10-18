def decode(self, encoded, parentFieldName=''):
    """ See the function description in base.py
    """

    # For now, we simply assume any top-down output greater than 0
    #  is ON. Eventually, we will probably want to incorporate the strength
    #  of each top-down output.
    tmpOutput = numpy.array(encoded[:self.n] > 0).astype(encoded.dtype)
    if not tmpOutput.any():
      return (dict(), [])

    # ------------------------------------------------------------------------
    # First, assume the input pool is not sampled 100%, and fill in the
    #  "holes" in the encoded representation (which are likely to be present
    #  if this is a coincidence that was learned by the SP).

    # Search for portions of the output that have "holes"
    maxZerosInARow = self.halfwidth
    for i in xrange(maxZerosInARow):
      searchStr = numpy.ones(i + 3, dtype=encoded.dtype)
      searchStr[1:-1] = 0
      subLen = len(searchStr)

      # Does this search string appear in the output?
      if self.periodic:
        for j in xrange(self.n):
          outputIndices = numpy.arange(j, j + subLen)
          outputIndices %= self.n
          if numpy.array_equal(searchStr, tmpOutput[outputIndices]):
            tmpOutput[outputIndices] = 1

      else:
        for j in xrange(self.n - subLen + 1):
          if numpy.array_equal(searchStr, tmpOutput[j:j + subLen]):
            tmpOutput[j:j + subLen] = 1


    if self.verbosity >= 2:
      print "raw output:", encoded[:self.n]
      print "filtered output:", tmpOutput

    # ------------------------------------------------------------------------
    # Find each run of 1's.
    nz = tmpOutput.nonzero()[0]
    runs = []     # will be tuples of (startIdx, runLength)
    run = [nz[0], 1]
    i = 1
    while (i < len(nz)):
      if nz[i] == run[0] + run[1]:
        run[1] += 1
      else:
        runs.append(run)
        run = [nz[i], 1]
      i += 1
    runs.append(run)

    # If we have a periodic encoder, merge the first and last run if they
    #  both go all the way to the edges
    if self.periodic and len(runs) > 1:
      if runs[0][0] == 0 and runs[-1][0] + runs[-1][1] == self.n:
        runs[-1][1] += runs[0][1]
        runs = runs[1:]


    # ------------------------------------------------------------------------
    # Now, for each group of 1's, determine the "left" and "right" edges, where
    #  the "left" edge is inset by halfwidth and the "right" edge is inset by
    #  halfwidth.
    # For a group of width w or less, the "left" and "right" edge are both at
    #   the center position of the group.
    ranges = []
    for run in runs:
      (start, runLen) = run
      if runLen <= self.w:
        left = right = start + runLen / 2
      else:
        left = start + self.halfwidth
        right = start + runLen - 1 - self.halfwidth

      # Convert to input space.
      if not self.periodic:
        inMin = (left - self.padding) * self.resolution + self.minval
        inMax = (right - self.padding) * self.resolution + self.minval
      else:
        inMin = (left - self.padding) * self.range / self.nInternal + self.minval
        inMax = (right - self.padding) * self.range / self.nInternal + self.minval
      # Handle wrap-around if periodic
      if self.periodic:
        if inMin >= self.maxval:
          inMin -= self.range
          inMax -= self.range

      # Clip low end
      if inMin < self.minval:
        inMin = self.minval
      if inMax < self.minval:
        inMax = self.minval

      # If we have a periodic encoder, and the max is past the edge, break into
      #  2 separate ranges
      if self.periodic and inMax >= self.maxval:
        ranges.append([inMin, self.maxval])
        ranges.append([self.minval, inMax - self.range])
      else:
        if inMax > self.maxval:
          inMax = self.maxval
        if inMin > self.maxval:
          inMin = self.maxval
        ranges.append([inMin, inMax])

    desc = self._generateRangeDescription(ranges)
    # Return result
    if parentFieldName != '':
      fieldName = "%s.%s" % (parentFieldName, self.name)
    else:
      fieldName = self.name

    return ({fieldName: (ranges, desc)}, [fieldName])