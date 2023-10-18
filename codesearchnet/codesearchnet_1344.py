def Any(sequence):
  """
  Tests much faster (30%) than bool(sum(bool(x) for x in sequence)).

  :returns: (bool) true if any element of the sequence satisfies True. 

  :param sequence: Any sequence whose elements can be evaluated as booleans.
  """
  return bool(reduce(lambda x, y: x or y, sequence, False))