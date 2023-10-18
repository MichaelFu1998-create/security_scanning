def mapCellsToColumns(self, cells):
    """
    Maps cells to the columns they belong to.

    :param cells: (set) Cells

    :returns: (dict) Mapping from columns to their cells in `cells`
    """
    cellsForColumns = defaultdict(set)

    for cell in cells:
      column = self.columnForCell(cell)
      cellsForColumns[column].add(cell)

    return cellsForColumns