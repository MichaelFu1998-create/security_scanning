def generateFromNumbers(self, numbers):
    """
    Generate a sequence from a list of numbers.

    Note: Any `None` in the list of numbers is considered a reset.

    @param numbers (list) List of numbers

    @return (list) Generated sequence
    """
    sequence = []

    for number in numbers:
      if number == None:
        sequence.append(number)
      else:
        pattern = self.patternMachine.get(number)
        sequence.append(pattern)

    return sequence