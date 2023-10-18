def aracne(m, **kwargs):
    """Implementation of the ARACNE algorithm.

    Args:
     mat (numpy.ndarray): matrix, if it is a square matrix, the program assumes
         it is a relevance matrix where mat(i,j) represents the similarity content
         between nodes i and j. Elements of matrix should be
         non-negative.

    Returns:
    mat_nd (numpy.ndarray): Output deconvolved matrix (direct dependency matrix). Its components
        represent direct edge weights of observed interactions.

    .. note::
       Ref: ARACNE: An Algorithm for the Reconstruction of Gene Regulatory Networks in a Mammalian Cellular Context
       Adam A Margolin, Ilya Nemenman, Katia Basso, Chris Wiggins, Gustavo Stolovitzky, Riccardo Dalla Favera and Andrea Califano
       DOI: https://doi.org/10.1186/1471-2105-7-S1-S7
    """
    I0 = kwargs.get('I0', 0.0)  # No default thresholding
    W0 = kwargs.get('W0', 0.05)

    # thresholding
    m = np.where(m > I0, m, 0)

    # Finding triplets and filtering them
    for i in range(m.shape[0]-2):
        for j in range(i+1, m.shape[0]-1):
            for k in range(j+1, m.shape[0]):
                triplet = [m[i, j], m[j, k], m[i, k]]
                min_index, min_value = min(enumerate(triplet), key=operator.itemgetter(1))
                if 0 < min_value < W0:
                    if min_index == 0:
                        m[i, j] = m[j, i] = 0.
                    elif min_index == 1:
                        m[j, k] = m[k, j] = 0.
                    else:
                        m[i, k] = m[k, i] = 0.
    return m