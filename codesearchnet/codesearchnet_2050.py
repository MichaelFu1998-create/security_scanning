def getrandbits(self, k):
    """getrandbits(k) -> x.  Generates an int with k random bits."""
    if k <= 0:
      raise ValueError('number of bits must be greater than zero')
    if k != int(k):
      raise TypeError('number of bits should be an integer')
    numbytes = (k + 7) // 8                       # bits / 8 and rounded up
    x = _int_from_bytes(_gorandom(numbytes))
    return x >> (numbytes * 8 - k)