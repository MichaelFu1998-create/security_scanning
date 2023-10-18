def get(self, number):
    """
    Return a pattern for a number.

    @param number (int) Number of pattern

    @return (set) Indices of on bits
    """
    if not number in self._patterns:
      raise IndexError("Invalid number")

    return self._patterns[number]