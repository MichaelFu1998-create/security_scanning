def handleInputRecord(self, inputRecord):
    """
    Processes the given record according to the current iteration cycle phase

    :param inputRecord: (object) record expected to be returned from
           :meth:`nupic.data.record_stream.RecordStreamIface.getNextRecord`.

    :returns: :class:`nupic.frameworks.opf.opf_utils.ModelResult`
    """
    assert inputRecord, "Invalid inputRecord: %r" % inputRecord

    results = self.__phaseManager.handleInputRecord(inputRecord)
    metrics = self.__metricsMgr.update(results)

    # Execute task-postIter callbacks
    for cb in self.__userCallbacks['postIter']:
      cb(self.__model)

    results.metrics = metrics

    # Return the input and predictions for this record
    return results