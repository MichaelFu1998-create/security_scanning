def csvd(A):
    """SVD decomposition using numpy.linalg.svd

    :param A: a M by N matrix

    :return:
        * U, a M by M matrix
        * S the N eigen values
        * V a N by N matrix

    See :func:`numpy.linalg.svd` for a detailed documentation.

    Should return the same as in [Marple]_ , CSVD routine.

    ::

        U, S, V = numpy.linalg.svd(A)
        U, S, V = cvsd(A)

    """
    U, S, V = numpy.linalg.svd(A)
    return U, S, V