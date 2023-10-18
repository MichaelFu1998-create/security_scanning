def _updateInhibitionRadius(self):
    """
    Update the inhibition radius. The inhibition radius is a measure of the
    square (or hypersquare) of columns that each a column is "connected to"
    on average. Since columns are are not connected to each other directly, we
    determine this quantity by first figuring out how many *inputs* a column is
    connected to, and then multiplying it by the total number of columns that
    exist for each input. For multiple dimension the aforementioned
    calculations are averaged over all dimensions of inputs and columns. This
    value is meaningless if global inhibition is enabled.
    """
    if self._globalInhibition:
      self._inhibitionRadius = int(self._columnDimensions.max())
      return

    avgConnectedSpan = numpy.average(
                          [self._avgConnectedSpanForColumnND(i)
                          for i in xrange(self._numColumns)]
                        )
    columnsPerInput = self._avgColumnsPerInput()
    diameter = avgConnectedSpan * columnsPerInput
    radius = (diameter - 1) / 2.0
    radius = max(1.0, radius)
    self._inhibitionRadius = int(radius + 0.5)