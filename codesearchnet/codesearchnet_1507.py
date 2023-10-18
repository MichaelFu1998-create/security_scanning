def handleInputRecord(self, inputRecord):
    """ Processes the given record according to the current phase

    inputRecord:  record object formatted according to
                  nupic.data.FileSource.getNext() result format.

    Returns:      An opf_utils.ModelResult object with the inputs and inferences
                  after the current record is processed by the model
    """

    results = self.__model.run(inputRecord)

    shouldContinue = self.__currentPhase.advance()
    if not shouldContinue:
      self.__advancePhase()

    return results