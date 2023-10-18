def setResultsPerChoice(self, resultsPerChoice):
    """Setup our resultsPerChoice history based on the passed in
    resultsPerChoice.

    For example, if this variable has the following choices:
      ['a', 'b', 'c']

    resultsPerChoice will have up to 3 elements, each element is a tuple
    containing (choiceValue, errors) where errors is the list of errors
    received from models that used the specific choice:
    retval:
      [('a', [0.1, 0.2, 0.3]), ('b', [0.5, 0.1, 0.6]), ('c', [0.2])]
    """
    # Keep track of the results obtained for each choice.
    self._resultsPerChoice = [[]] * len(self.choices)
    for (choiceValue, values) in resultsPerChoice:
      choiceIndex = self.choices.index(choiceValue)
      self._resultsPerChoice[choiceIndex] = list(values)