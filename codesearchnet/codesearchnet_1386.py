def createInput(self):
    """create a random input vector"""

    print "-" * 70 + "Creating a random input vector" + "-" * 70

    #clear the inputArray to zero before creating a new input vector
    self.inputArray[0:] = 0

    for i in range(self.inputSize):
      #randrange returns 0 or 1
      self.inputArray[i] = random.randrange(2)