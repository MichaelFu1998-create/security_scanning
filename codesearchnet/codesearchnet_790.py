def replace(self, columnIndex, bitmap):
    """ Wraps replaceSparseRow()"""
    return super(_SparseMatrixCorticalColumnAdapter, self).replaceSparseRow(
      columnIndex, bitmap
    )