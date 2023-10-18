def economic_qs_zeros(n):
    """Eigen decomposition of a zero matrix."""

    Q0 = empty((n, 0))
    Q1 = eye(n)
    S0 = empty(0)

    return ((Q0, Q1), S0)