def network_deconvolution(mat, **kwargs):
    """Python implementation/translation of network deconvolution by MIT-KELLIS LAB.

    .. note::
       code author:gidonro [Github username](https://github.com/gidonro/Network-Deconvolution)

       LICENSE: MIT-KELLIS LAB

       AUTHORS:
       Algorithm was programmed by Soheil Feizi.
       Paper authors are S. Feizi, D. Marbach,  M. M?©dard and M. Kellis
       Python implementation: Gideon Rosenthal

       For more details, see the following paper:
       Network Deconvolution as a General Method to Distinguish
       Direct Dependencies over Networks

       By: Soheil Feizi, Daniel Marbach,  Muriel Médard and Manolis Kellis
       Nature Biotechnology

    Args:
     mat (numpy.ndarray): matrix, if it is a square matrix, the program assumes
         it is a relevance matrix where mat(i,j) represents the similarity content
         between nodes i and j. Elements of matrix should be
         non-negative.
     beta (float): Scaling parameter, the program maps the largest absolute eigenvalue
         of the direct dependency matrix to beta. It should be
         between 0 and 1.
     alpha (float): fraction of edges of the observed dependency matrix to be kept in
         deconvolution process.
     control (int): if 0, displaying direct weights for observed
         interactions, if 1, displaying direct weights for both observed and
         non-observed interactions.

    Returns:
    mat_nd (numpy.ndarray): Output deconvolved matrix (direct dependency matrix). Its components
        represent direct edge weights of observed interactions.
        Choosing top direct interactions (a cut-off) depends on the application and
        is not implemented in this code.

     .. note::
        To apply ND on regulatory networks, follow steps explained in Supplementary notes
        1.4.1 and 2.1 and 2.3 of the paper.
        In this implementation, input matrices are made symmetric.
    """
    alpha = kwargs.get('alpha', 1)
    beta = kwargs.get('beta', 0.99)
    control = kwargs.get('control', 0)

    # ToDO : ASSERTS
    try:
        assert beta < 1 or beta > 0
        assert alpha <= 1 or alpha > 0

    except AssertionError:
        raise ValueError("alpha must be in ]0, 1] and beta in [0, 1]")

    #  Processing the input matrix, diagonal values are filtered
    np.fill_diagonal(mat, 0)

    # Thresholding the input matrix
    y = stat.mquantiles(mat[:], prob=[1 - alpha])
    th = mat >= y
    mat_th = mat * th

    # Making the matrix symetric if already not
    mat_th = (mat_th + mat_th.T) / 2

    # Eigen decomposition
    Dv, U = LA.eigh(mat_th)
    D = np.diag((Dv))
    lam_n = np.abs(np.min(np.min(np.diag(D)), 0))
    lam_p = np.abs(np.max(np.max(np.diag(D)), 0))

    m1 = lam_p * (1 - beta) / beta
    m2 = lam_n * (1 + beta) / beta
    m = max(m1, m2)

    # network deconvolution
    for i in range(D.shape[0]):
        D[i, i] = (D[i, i]) / (m + D[i, i])

    mat_new1 = np.dot(U, np.dot(D, LA.inv(U)))

    # Displying direct weights

    if control == 0:
        ind_edges = (mat_th > 0) * 1.0
        ind_nonedges = (mat_th == 0) * 1.0
        m1 = np.max(np.max(mat * ind_nonedges))
        m2 = np.min(np.min(mat_new1))
        mat_new2 = (mat_new1 + np.max(m1 - m2, 0)) * ind_edges + (mat * ind_nonedges)
    else:
        m2 = np.min(np.min(mat_new1))
        mat_new2 = (mat_new1 + np.max(-m2, 0))

    # linearly mapping the deconvolved matrix to be between 0 and 1
    m1 = np.min(np.min(mat_new2))
    m2 = np.max(np.max(mat_new2))
    mat_nd = (mat_new2 - m1) / (m2 - m1)

    return mat_nd