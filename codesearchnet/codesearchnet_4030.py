def clr(M, **kwargs):
    """Implementation of the Context Likelihood or Relatedness Network algorithm.

    Args:
     mat (numpy.ndarray): matrix, if it is a square matrix, the program assumes
         it is a relevance matrix where mat(i,j) represents the similarity content
         between nodes i and j. Elements of matrix should be
         non-negative.

    Returns:
    mat_nd (numpy.ndarray): Output deconvolved matrix (direct dependency matrix). Its components
        represent direct edge weights of observed interactions.

    .. note::
       Ref:Jeremiah J. Faith, Boris Hayete, Joshua T. Thaden, Ilaria Mogno, Jamey
       Wierzbowski, Guillaume Cottarel, Simon Kasif, James J. Collins, and Timothy
       S. Gardner. Large-scale mapping and validation of escherichia coli
       transcriptional regulation from a compendium of expression profiles.
       PLoS Biology, 2007
    """
    R = np.zeros(M.shape)
    Id = [[0, 0] for i in range(M.shape[0])]
    for i in range(M.shape[0]):
        mu_i = np.mean(M[i, :])
        sigma_i = np.std(M[i, :])
        Id[i] = [mu_i, sigma_i]

    for i in range(M.shape[0]):
        for j in range(i + 1, M.shape[0]):
            z_i = np.max([0, (M[i, j] - Id[i][0]) / Id[i][0]])
            z_j = np.max([0, (M[i, j] - Id[j][0]) / Id[j][0]])
            R[i, j] = np.sqrt(z_i**2 + z_j**2)
            R[j, i] = R[i, j]  # Symmetric

    return R