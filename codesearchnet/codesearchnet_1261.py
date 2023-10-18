def shift(self, modelResult):
    """Shift the model result and return the new instance.

    Queues up the T(i+1) prediction value and emits a T(i)
    input/prediction pair, if possible. E.g., if the previous T(i-1)
    iteration was learn-only, then we would not have a T(i) prediction in our
    FIFO and would not be able to emit a meaningful input/prediction pair.

    :param modelResult: A :class:`~.nupic.frameworks.opf.opf_utils.ModelResult`
                        instance to shift.
    :return: A :class:`~.nupic.frameworks.opf.opf_utils.ModelResult` instance that
             has been shifted
    """
    inferencesToWrite = {}

    if self._inferenceBuffer is None:
      maxDelay = InferenceElement.getMaxDelay(modelResult.inferences)
      self._inferenceBuffer = collections.deque(maxlen=maxDelay + 1)

    self._inferenceBuffer.appendleft(copy.deepcopy(modelResult.inferences))

    for inferenceElement, inference in modelResult.inferences.iteritems():
      if isinstance(inference, dict):
        inferencesToWrite[inferenceElement] = {}
        for key, _ in inference.iteritems():
          delay = InferenceElement.getTemporalDelay(inferenceElement, key)
          if len(self._inferenceBuffer) > delay:
            prevInference = self._inferenceBuffer[delay][inferenceElement][key]
            inferencesToWrite[inferenceElement][key] = prevInference
          else:
            inferencesToWrite[inferenceElement][key] = None
      else:
        delay = InferenceElement.getTemporalDelay(inferenceElement)
        if len(self._inferenceBuffer) > delay:
          inferencesToWrite[inferenceElement] = (
              self._inferenceBuffer[delay][inferenceElement])
        else:
          if type(inference) in (list, tuple):
            inferencesToWrite[inferenceElement] = [None] * len(inference)
          else:
            inferencesToWrite[inferenceElement] = None

    shiftedResult = ModelResult(rawInput=modelResult.rawInput,
                                sensorInput=modelResult.sensorInput,
                                inferences=inferencesToWrite,
                                metrics=modelResult.metrics,
                                predictedFieldIdx=modelResult.predictedFieldIdx,
                                predictedFieldName=modelResult.predictedFieldName)
    return shiftedResult