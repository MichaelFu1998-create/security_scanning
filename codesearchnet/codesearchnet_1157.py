def addNoise(self, bits, amount):
    """
    Add noise to pattern.

    @param bits   (set)   Indices of on bits
    @param amount (float) Probability of switching an on bit with a random bit

    @return (set) Indices of on bits in noisy pattern
    """
    newBits = set()

    for bit in bits:
      if self._random.getReal64() < amount:
        newBits.add(self._random.getUInt32(self._n))
      else:
        newBits.add(bit)

    return newBits