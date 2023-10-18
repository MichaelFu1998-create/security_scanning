def birkhoff_von_neumann_decomposition(D):
    """Returns the Birkhoff--von Neumann decomposition of the doubly
    stochastic matrix `D`.

    The input `D` must be a square NumPy array representing a doubly
    stochastic matrix (that is, a matrix whose entries are nonnegative
    reals and whose row sums and column sums are all 1). Each doubly
    stochastic matrix is a convex combination of at most ``n ** 2``
    permutation matrices, where ``n`` is the dimension of the input
    array.

    The returned value is a list of pairs whose length is at most ``n **
    2``. In each pair, the first element is a real number in the interval **(0,
    1]** and the second element is a NumPy array representing a permutation
    matrix. This represents the doubly stochastic matrix as a convex
    combination of the permutation matrices.

    The input matrix may also be a scalar multiple of a doubly
    stochastic matrix, in which case the row sums and column sums must
    each be *c*, for some positive real number *c*. This may be useful
    in avoiding precision issues: given a doubly stochastic matrix that
    will have many entries close to one, multiply it by a large positive
    integer. The returned permutation matrices will be the same
    regardless of whether the given matrix is a doubly stochastic matrix
    or a scalar multiple of a doubly stochastic matrix, but in the
    latter case, the coefficients will all be scaled by the appropriate
    scalar multiple, and their sum will be that scalar instead of one.

    For example::

        >>> import numpy as np
        >>> from birkhoff import birkhoff_von_neumann_decomposition as decomp
        >>> D = np.ones((2, 2))
        >>> zipped_pairs = decomp(D)
        >>> coefficients, permutations = zip(*zipped_pairs)
        >>> coefficients
        (1.0, 1.0)
        >>> permutations[0]
        array([[ 1.,  0.],
               [ 0.,  1.]])
        >>> permutations[1]
        array([[ 0.,  1.],
               [ 1.,  0.]])
        >>> zipped_pairs = decomp(D / 2)  # halve each value in the matrix
        >>> coefficients, permutations = zip(*zipped_pairs)
        >>> coefficients  # will be half as large as before
        (0.5, 0.5)
        >>> permutations[0]  # will be the same as before
        array([[ 1.,  0.],
               [ 0.,  1.]])
        >>> permutations[1]
        array([[ 0.,  1.],
               [ 1.,  0.]])

    The returned list of pairs is given in the order computed by the algorithm
    (so in particular they are not sorted in any way).

    """
    m, n = D.shape
    if m != n:
        raise ValueError('Input matrix must be square ({} x {})'.format(m, n))
    indices = list(itertools.product(range(m), range(n)))
    # These two lists will store the result as we build it up each iteration.
    coefficients = []
    permutations = []
    # Create a copy of D so that we don't modify it directly. Cast the
    # entries of the matrix to floating point numbers, regardless of
    # whether they were integers.
    S = D.astype('float')
    while not np.all(S == 0):
        # Create an undirected graph whose adjacency matrix contains a 1
        # exactly where the matrix S has a nonzero entry.
        W = to_pattern_matrix(S)
        # Construct the bipartite graph whose left and right vertices both
        # represent the vertex set of the pattern graph (whose adjacency matrix
        # is ``W``).
        X = to_bipartite_matrix(W)
        # Convert the matrix of a bipartite graph into a NetworkX graph object.
        G = from_numpy_matrix(X)
        # Compute a perfect matching for this graph. The dictionary `M` has one
        # entry for each matched vertex (in both the left and the right vertex
        # sets), and the corresponding value is its partner.
        #
        # The bipartite maximum matching algorithm requires specifying
        # the left set of nodes in the bipartite graph. By construction,
        # the left set of nodes is {0, ..., n - 1} and the right set is
        # {n, ..., 2n - 1}; see `to_bipartite_matrix()`.
        left_nodes = range(n)
        M = maximum_matching(G, left_nodes)
        # However, since we have both a left vertex set and a right vertex set,
        # each representing the original vertex set of the pattern graph
        # (``W``), we need to convert any vertex greater than ``n`` to its
        # original vertex number. To do this,
        #
        #   - ignore any keys greater than ``n``, since they are already
        #     covered by earlier key/value pairs,
        #   - ensure that all values are less than ``n``.
        #
        M = {u: v % n for u, v in M.items() if u < n}
        # Convert that perfect matching to a permutation matrix.
        P = to_permutation_matrix(M)
        # Get the smallest entry of S corresponding to the 1 entries in the
        # permutation matrix.
        q = min(S[i, j] for (i, j) in indices if P[i, j] == 1)
        # Store the coefficient and the permutation matrix for later.
        coefficients.append(q)
        permutations.append(P)
        # Subtract P scaled by q. After this subtraction, S has a zero entry
        # where the value q used to live.
        S -= q * P
        # PRECISION ISSUE: There seems to be a problem with floating point
        # precision here, so we need to round down to 0 any entry that is very
        # small.
        S[np.abs(S) < TOLERANCE] = 0.0
    return list(zip(coefficients, permutations))