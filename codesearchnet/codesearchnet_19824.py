def matrixValues(matrix,key):
    """given a key, return a list of values from the matrix with that key."""
    assert key in matrix.dtype.names
    col=matrix.dtype.names.index(key)
    values=np.empty(len(matrix))*np.nan
    for i in range(len(matrix)):
        values[i]=matrix[i][col]
    return values