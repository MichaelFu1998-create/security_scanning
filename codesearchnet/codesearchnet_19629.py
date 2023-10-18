def to_permutation_matrix(matches):
    """Converts a permutation into a permutation matrix.

    `matches` is a dictionary whose keys are vertices and whose values are
    partners. For each vertex ``u`` and ``v``, entry (``u``, ``v``) in the
    returned matrix will be a ``1`` if and only if ``matches[u] == v``.

    Pre-condition: `matches` must be a permutation on an initial subset of the
    natural numbers.

    Returns a permutation matrix as a square NumPy array.

    """
    n = len(matches)
    P = np.zeros((n, n))
    # This is a cleverer way of doing
    #
    #     for (u, v) in matches.items():
    #         P[u, v] = 1
    #
    P[list(zip(*(matches.items())))] = 1
    return P