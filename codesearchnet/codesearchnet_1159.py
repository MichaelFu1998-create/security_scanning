def numberMapForBits(self, bits):
    """
    Return a map from number to matching on bits,
    for all numbers that match a set of bits.

    @param bits (set) Indices of bits

    @return (dict) Mapping from number => on bits.
    """
    numberMap = dict()

    for bit in bits:
      numbers = self.numbersForBit(bit)

      for number in numbers:
        if not number in numberMap:
          numberMap[number] = set()

        numberMap[number].add(bit)

    return numberMap