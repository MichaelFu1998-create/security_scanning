def _getColumnNeighborhood(self, centerColumn):
    """
    Gets a neighborhood of columns.

    Simply calls topology.neighborhood or topology.wrappingNeighborhood

    A subclass can insert different topology behavior by overriding this method.

    :param centerColumn (int)
    The center of the neighborhood.

    @returns (1D numpy array of integers)
    The columns in the neighborhood.
    """
    if self._wrapAround:
      return topology.wrappingNeighborhood(centerColumn,
                                           self._inhibitionRadius,
                                           self._columnDimensions)

    else:
      return topology.neighborhood(centerColumn,
                                   self._inhibitionRadius,
                                   self._columnDimensions)