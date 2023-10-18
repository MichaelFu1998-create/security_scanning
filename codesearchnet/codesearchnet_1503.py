def _getImpl(self, model):
    """ Creates and returns the _IterationPhase-based instance corresponding
    to this phase specification

    model:          Model instance
    """
    impl = _IterationPhaseInferOnly(model=model,
                                    nIters=self.__nIters,
                                    inferenceArgs=self.__inferenceArgs)
    return impl