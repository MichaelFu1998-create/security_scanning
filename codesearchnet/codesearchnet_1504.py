def replaceIterationCycle(self, phaseSpecs):
    """ Replaces the Iteration Cycle phases

    :param phaseSpecs: Iteration cycle description consisting of a sequence of
                  IterationPhaseSpecXXXXX elements that are performed in the
                  given order
    """

    # -----------------------------------------------------------------------
    # Replace our phase manager
    #
    self.__phaseManager = _PhaseManager(
      model=self.__model,
      phaseSpecs=phaseSpecs)

    return