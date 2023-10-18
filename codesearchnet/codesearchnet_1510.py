def enterPhase(self):
    """ [_IterationPhase method implementation]
    Performs initialization that is necessary upon entry to the phase. Must
    be called before handleInputRecord() at the beginning of each phase
    """
    super(_IterationPhaseLearnOnly, self).enterPhase()
    self.__model.enableLearning()
    self.__model.disableInference()
    return