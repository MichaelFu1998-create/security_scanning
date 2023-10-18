def _initializeEphemeralMembers(self):
    """
    Initialize all ephemeral data members, and give the derived class the
    opportunity to do the same by invoking the virtual member _initEphemerals(),
    which is intended to be overridden.

    NOTE: this is used by both __init__ and __setstate__ code paths.
    """

    for attrName in self._getEphemeralMembersBase():
      if attrName != "_loaded":
        if hasattr(self, attrName):
          if self._loaded:
            # print self.__class__.__name__, "contains base class member '%s' " \
            #     "after loading." % attrName
            # TODO: Re-enable warning or turn into error in a future release.
            pass
          else:
            print self.__class__.__name__, "contains base class member '%s'" % \
                attrName
    if not self._loaded:
      for attrName in self._getEphemeralMembersBase():
        if attrName != "_loaded":
          # if hasattr(self, attrName):
          #   import pdb; pdb.set_trace()
          assert not hasattr(self, attrName)
        else:
          assert hasattr(self, attrName)

    # Profiling information
    self._profileObj = None
    self._iterations = 0

    # Let derived class initialize ephemerals
    self._initEphemerals()
    self._checkEphemeralMembers()