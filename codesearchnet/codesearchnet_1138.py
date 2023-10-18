def finalize(self):
    """Close file and print report/backup csv file paths

    Parameters:
    ----------------------------------------------------------------------
    retval:         nothing
    """
    if self.__csvFileObj is not None:
      # Done with file
      self.__csvFileObj.close()
      self.__csvFileObj = None

      print "Report csv saved in %s" % (self.__reportCSVPath,)

      if self.__backupCSVPath:
        print "Previous report csv file was backed up to %s" % \
                (self.__backupCSVPath,)
    else:
      print "Nothing was written to report csv file."