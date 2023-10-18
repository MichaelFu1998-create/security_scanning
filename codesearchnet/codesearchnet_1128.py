def pickupSearch(self):
    """Pick up the latest search from a saved jobID and monitor it to completion
    Parameters:
    ----------------------------------------------------------------------
    retval:         nothing
    """
    self.__searchJob = self.loadSavedHyperSearchJob(
      permWorkDir=self._options["permWorkDir"],
      outputLabel=self._options["outputLabel"])


    self.monitorSearchJob()