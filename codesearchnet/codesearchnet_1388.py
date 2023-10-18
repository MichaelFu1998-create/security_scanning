def addNoise(self, noiseLevel):
    """Flip the value of 10% of input bits (add noise)

    :param noiseLevel: The percentage of total input bits that should be flipped
    """

    for _ in range(int(noiseLevel * self.inputSize)):
      # 0.1*self.inputSize represents 10% of the total input bits
      # random.random() returns a float between 0 and 1
      randomPosition = int(random.random() * self.inputSize)

      # Flipping the bit at the randomly picked position
      if self.inputArray[randomPosition] == 1:
        self.inputArray[randomPosition] = 0

      else:
        self.inputArray[randomPosition] = 1