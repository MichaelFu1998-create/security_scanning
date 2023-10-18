def getTerminationCallbacks(self, terminationFunc):
    """ Returns the periodic checks to see if the model should
    continue running.

    Parameters:
    -----------------------------------------------------------------------
    terminationFunc:  The function that will be called in the model main loop
                      as a wrapper around this function. Must have a parameter
                      called 'index'

    Returns:          A list of PeriodicActivityRequest objects.
    """
    activities = [None] * len(ModelTerminator._MILESTONES)
    for index, (iteration, _) in enumerate(ModelTerminator._MILESTONES):
      cb = functools.partial(terminationFunc, index=index)
      activities[index] = PeriodicActivityRequest(repeating =False,
                                                  period = iteration,
                                                  cb=cb)