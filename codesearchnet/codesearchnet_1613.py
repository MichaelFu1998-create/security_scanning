def getColCellIdx(self, idx):
    """
    Get column and cell within column from a global cell index.
    The global index is ``idx = colIdx * nCellsPerCol() + cellIdxInCol``
    
    :param idx: (int) global cell index
    :returns: (tuple) (colIdx, cellIdxInCol)
    """
    c = idx//self.cellsPerColumn
    i = idx - c*self.cellsPerColumn
    return c,i