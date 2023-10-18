def enterPhase(self):
    """ [_IterationPhase method implementation]
    Performs initialization that is necessary upon entry to the phase. Must
    be called before handleInputRecord() at the beginning of each phase
    """
    super(_IterationPhaseInferCommon, self).enterPhase()
    self._model.enableInference(inferenceArgs=self._inferenceArgs)
    return