def _initPeriodicActivities(self):
    """ Creates and returns a PeriodicActivityMgr instance initialized with
    our periodic activities

    Parameters:
    -------------------------------------------------------------------------
    retval:             a PeriodicActivityMgr instance
    """

    # Activity to update the metrics for this model
    # in the models table
    updateModelDBResults = PeriodicActivityRequest(repeating=True,
                                                 period=100,
                                                 cb=self._updateModelDBResults)

    updateJobResults = PeriodicActivityRequest(repeating=True,
                                               period=100,
                                               cb=self.__updateJobResultsPeriodic)

    checkCancelation = PeriodicActivityRequest(repeating=True,
                                               period=50,
                                               cb=self.__checkCancelation)

    checkMaturity = PeriodicActivityRequest(repeating=True,
                                            period=10,
                                            cb=self.__checkMaturity)


    # Do an initial update of the job record after 2 iterations to make
    # sure that it is populated with something without having to wait too long
    updateJobResultsFirst = PeriodicActivityRequest(repeating=False,
                                               period=2,
                                               cb=self.__updateJobResultsPeriodic)


    periodicActivities = [updateModelDBResults,
                          updateJobResultsFirst,
                          updateJobResults,
                          checkCancelation]

    if self._isMaturityEnabled:
      periodicActivities.append(checkMaturity)

    return PeriodicActivityMgr(requestedActivities=periodicActivities)