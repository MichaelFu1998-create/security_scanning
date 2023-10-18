def _labelListToCategoryNumber(self, labelList):
    """
    This method takes a list of labels and returns a unique category number.
    This enables this class to store a list of categories for each point since
    the KNN classifier only stores a single number category for each record.
    """
    categoryNumber = 0
    for label in labelList:
      categoryNumber += self._labelToCategoryNumber(label)
    return categoryNumber