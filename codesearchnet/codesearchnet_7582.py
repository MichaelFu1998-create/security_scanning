def _numpy_cholesky(A, B):
    """Solve Ax=B using numpy cholesky solver

    A = LU

    in the case where A is square and Hermitian, A = L.L* where L* is
    transpoed and conjugate matrix

    Ly = b

    where

    Ux=y

    so x = U^{-1} y
    where U = L*
    and y = L^{-1} B
    """
    L = numpy.linalg.cholesky(A)
    # A=L*numpy.transpose(L).conjugate()
    # Ly = b
    y = numpy.linalg.solve(L,B)
    # Ux = y
    x = numpy.linalg.solve(L.transpose().conjugate(),y)
    return x, L