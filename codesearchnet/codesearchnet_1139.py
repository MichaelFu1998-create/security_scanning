def __openAndInitCSVFile(self, modelInfo):
    """
    - Backs up old report csv file;
    - opens the report csv file in append or overwrite mode (per
      self.__replaceReport);
    - emits column fields;
    - sets up self.__sortedVariableNames, self.__csvFileObj,
      self.__backupCSVPath, and self.__reportCSVPath

    Parameters:
    ----------------------------------------------------------------------
    modelInfo:      First _NupicModelInfo instance passed to emit()
    retval:         nothing
    """
    # Get the base path and figure out the path of the report file.
    basePath = self.__outputDirAbsPath

    # Form the name of the output csv file that will contain all the results
    reportCSVName = "%s_Report.csv" % (self.__outputLabel,)
    reportCSVPath = self.__reportCSVPath = os.path.join(basePath, reportCSVName)

    # If a report CSV file already exists, back it up
    backupCSVPath = None
    if os.path.exists(reportCSVPath):
      backupCSVPath = self.__backupCSVPath = _backupFile(reportCSVPath)


    # Open report file
    if self.__replaceReport:
      mode = "w"
    else:
      mode = "a"
    csv = self.__csvFileObj = open(reportCSVPath, mode)

    # If we are appending, add some blank line separators
    if not self.__replaceReport and backupCSVPath:
      print >> csv
      print >> csv

    # Print the column names
    print >> csv, "jobID, ",
    print >> csv, "modelID, ",
    print >> csv, "status, " ,
    print >> csv, "completionReason, ",
    print >> csv, "startTime, ",
    print >> csv, "endTime, ",
    print >> csv, "runtime(s), " ,
    print >> csv, "expDesc, ",
    print >> csv, "numRecords, ",

    for key in self.__sortedVariableNames:
      print >> csv, "%s, " % key,
    for key in self.__sortedMetricsKeys:
      print >> csv, "%s, " % key,
    print >> csv