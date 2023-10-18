def addSpatialNoise(self, sequence, amount):
    """
    Add spatial noise to each pattern in the sequence.

    @param sequence (list)  Sequence
    @param amount   (float) Amount of spatial noise

    @return (list) Sequence with spatial noise
    """
    newSequence = []

    for pattern in sequence:
      if pattern is not None:
        pattern = self.patternMachine.addNoise(pattern, amount)
      newSequence.append(pattern)

    return newSequence