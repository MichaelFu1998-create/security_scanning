def numbersForBit(self, bit):
    """
    Return the set of pattern numbers that match a bit.

    @param bit (int) Index of bit

    @return (set) Indices of numbers
    """
    if bit >= self._n:
      raise IndexError("Invalid bit")

    numbers = set()

    for index, pattern in self._patterns.iteritems():
      if bit in pattern:
        numbers.add(index)

    return numbers