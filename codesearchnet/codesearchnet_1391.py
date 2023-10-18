def prototypeSetCategory(self, idToCategorize, newCategory):
    """
    Allows ids to be assigned a category and subsequently enables users to use:

      - :meth:`~.KNNClassifier.KNNClassifier.removeCategory`
      - :meth:`~.KNNClassifier.KNNClassifier.closestTrainingPattern`
      - :meth:`~.KNNClassifier.KNNClassifier.closestOtherTrainingPattern`
    """
    if idToCategorize not in self._categoryRecencyList:
      return

    recordIndex = self._categoryRecencyList.index(idToCategorize)
    self._categoryList[recordIndex] = newCategory