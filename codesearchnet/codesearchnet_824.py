def handleGetValue(self, topContainer):
    """ This method overrides ValueGetterBase's "pure virtual" method.  It
    returns the referenced value.  The derived class is NOT responsible for
    fully resolving the reference'd value in the event the value resolves to
    another ValueGetterBase-based instance -- this is handled automatically
    within ValueGetterBase implementation.

    topContainer: The top-level container (dict, tuple, or list [sub-]instance)
                  within whose context the value-getter is applied.  If
                  self.__referenceDict is None, then topContainer will be used
                  as the reference dictionary for resolving our dictionary key
                  chain.

    Returns:      The value referenced by this instance (which may be another
                  value-getter instance)
    """
    value = self.__referenceDict if self.__referenceDict is not None else topContainer
    for key in self.__dictKeyChain:
      value = value[key]

    return value