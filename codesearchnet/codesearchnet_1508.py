def enterPhase(self):
    """
    Performs initialization that is necessary upon entry to the phase. Must
    be called before handleInputRecord() at the beginning of each phase
    """

    self.__iter = iter(xrange(self.__nIters))

    # Prime the iterator
    self.__iter.next()