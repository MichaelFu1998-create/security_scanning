def _countOverlap(rep1, rep2):
    """
    Return the overlap between two representations. rep1 and rep2 are lists of
    non-zero indices.
    """
    overlap = 0
    for e in rep1:
      if e in rep2:
        overlap += 1
    return overlap