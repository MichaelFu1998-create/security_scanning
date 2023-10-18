def emit(self, modelInfo):
    """Emit model info to csv file

    Parameters:
    ----------------------------------------------------------------------
    modelInfo:      _NupicModelInfo instance
    retval:         nothing
    """
    # Open/init csv file, if needed
    if self.__csvFileObj is None:
      # sets up self.__sortedVariableNames and self.__csvFileObj
      self.__openAndInitCSVFile(modelInfo)

    csv = self.__csvFileObj

    # Emit model info row to report.csv
    print >> csv, "%s, " % (self.__searchJobID),
    print >> csv, "%s, " % (modelInfo.getModelID()),
    print >> csv, "%s, " % (modelInfo.statusAsString()),
    if modelInfo.isFinished():
      print >> csv, "%s, " % (modelInfo.getCompletionReason()),
    else:
      print >> csv, "NA, ",
    if not modelInfo.isWaitingToStart():
      print >> csv, "%s, " % (modelInfo.getStartTime()),
    else:
      print >> csv, "NA, ",
    if modelInfo.isFinished():
      dateFormat = "%Y-%m-%d %H:%M:%S"
      startTime = modelInfo.getStartTime()
      endTime = modelInfo.getEndTime()
      print >> csv, "%s, " % endTime,
      st = datetime.strptime(startTime, dateFormat)
      et = datetime.strptime(endTime, dateFormat)
      print >> csv, "%s, " % (str((et - st).seconds)),
    else:
      print >> csv, "NA, ",
      print >> csv, "NA, ",
    print >> csv, "%s, " % str(modelInfo.getModelDescription()),
    print >> csv, "%s, " % str(modelInfo.getNumRecords()),
    paramLabelsDict = modelInfo.getParamLabels()
    for key in self.__sortedVariableNames:
      # Some values are complex structures,.. which need to be represented as
      # strings
      if key in paramLabelsDict:
        print >> csv, "%s, " % (paramLabelsDict[key]),
      else:
        print >> csv, "None, ",
    metrics = modelInfo.getReportMetrics()
    for key in self.__sortedMetricsKeys:
      value = metrics.get(key, "NA")
      value = str(value)
      value = value.replace("\n", " ")
      print >> csv, "%s, " % (value),

    print >> csv