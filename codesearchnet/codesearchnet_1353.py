def transferCoincidences(network, fromElementName, toElementName):
  """
  Gets the coincidence matrix from one element and sets it on
  another element
  (using locked handles, a la nupic.bindings.research.lockHandle).

  TODO: Generalize to more node types, parameter name pairs, etc.

  Does not work across processes.
  """
  coincidenceHandle = getLockedHandle(
      runtimeElement=network.getElement(fromElementName),
      # TODO: Re-purpose for use with nodes other than PMXClassifierNode.
      expression="self._cd._W"
    )

  network.getElement(toElementName).setParameter("coincidencesAbove",
      coincidenceHandle)