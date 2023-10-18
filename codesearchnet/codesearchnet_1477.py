def columnForCell(self, cell):
    """
    Returns the index of the column that a cell belongs to.

    :param cell: (int) Cell index

    :returns: (int) Column index
    """
    self._validateCell(cell)

    return int(cell / self.cellsPerColumn)