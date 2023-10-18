def stripUnlearnedColumns(self, activeArray):
    """
    Removes the set of columns who have never been active from the set of
    active columns selected in the inhibition round. Such columns cannot
    represent learned pattern and are therefore meaningless if only inference
    is required. This should not be done when using a random, unlearned SP
    since you would end up with no active columns.

    :param activeArray: An array whose size is equal to the number of columns.
        Any columns marked as active with an activeDutyCycle of 0 have
        never been activated before and therefore are not active due to
        learning. Any of these (unlearned) columns will be disabled (set to 0).
    """
    neverLearned = numpy.where(self._activeDutyCycles == 0)[0]
    activeArray[neverLearned] = 0