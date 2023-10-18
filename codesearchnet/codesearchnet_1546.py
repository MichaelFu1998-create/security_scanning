def run(self, inputRecord):
    """
    Run one iteration of this model.

    :param inputRecord: (object)
           A record object formatted according to
           :meth:`~nupic.data.record_stream.RecordStreamIface.getNextRecord` or
           :meth:`~nupic.data.record_stream.RecordStreamIface.getNextRecordDict`
           result format.
    :returns: (:class:`~nupic.frameworks.opf.opf_utils.ModelResult`)
             An ModelResult namedtuple. The contents of ModelResult.inferences
             depends on the the specific inference type of this model, which
             can be queried by :meth:`.getInferenceType`.
    """
    # 0-based prediction index for ModelResult
    predictionNumber = self._numPredictions
    self._numPredictions += 1
    result = opf_utils.ModelResult(predictionNumber=predictionNumber,
                                   rawInput=inputRecord)
    return result