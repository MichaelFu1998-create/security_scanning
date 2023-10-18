def __appendActivities(self, periodicActivities):
    """
    periodicActivities: A sequence of PeriodicActivityRequest elements
    """

    for req in periodicActivities:
      act =   self.Activity(repeating=req.repeating,
                            period=req.period,
                            cb=req.cb,
                            iteratorHolder=[iter(xrange(req.period-1))])
      self.__activities.append(act)

    return