def __advancePhase(self):
    """ Advance to the next iteration cycle phase
    """
    self.__currentPhase = self.__phaseCycler.next()
    self.__currentPhase.enterPhase()

    return