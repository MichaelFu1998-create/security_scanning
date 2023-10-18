def _document_frequency(X):
    """
    Count the number of non-zero values for each feature in sparse X.
    """
    if sp.isspmatrix_csr(X):
        return np.bincount(X.indices, minlength=X.shape[1])
    return np.diff(sp.csc_matrix(X, copy=False).indptr)