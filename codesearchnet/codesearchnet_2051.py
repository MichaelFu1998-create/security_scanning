def _randbelow(self, n):
    """Return a random int in the range [0,n)."""
    # TODO
    # change once int.bit_length is implemented.
    # k = n.bit_length()
    k = _int_bit_length(n)
    r = self.getrandbits(k)
    while r >= n:
      r = self.getrandbits(k)
    return r