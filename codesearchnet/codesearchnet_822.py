def _getInputNeighborhood(self, centerInput):
    """
    Gets a neighborhood of inputs.

    Simply calls topology.wrappingNeighborhood or topology.neighborhood.

    A subclass can insert different topology behavior by overriding this method.

    :param centerInput (int)
    The center of the neighborhood.

    @returns (1D numpy array of integers)
    The inputs in the neighborhood.
    """
    if self._wrapAround:
      return topology.wrappingNeighborhood(centerInput,
                                           self._potentialRadius,
                                           self._inputDimensions)
    else:
      return topology.neighborhood(centerInput,
                                   self._potentialRadius,
                                   self._inputDimensions)