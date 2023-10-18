def update(self, columnIndex, vector):
    """ Wraps setRowFromDense()"""
    return super(_SparseMatrixCorticalColumnAdapter, self).setRowFromDense(
      columnIndex, vector
    )