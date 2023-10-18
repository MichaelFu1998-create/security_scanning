def cellsForColumn(self, column):
    """
    Returns the indices of cells that belong to a column.

    :param column: (int) Column index

    :returns: (list) Cell indices
    """
    self._validateColumn(column)

    start = self.cellsPerColumn * column
    end = start + self.cellsPerColumn
    return range(start, end)