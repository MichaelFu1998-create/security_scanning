def _matrix2dict(matrix, etype=False):
    """Takes an adjacency matrix and returns an adjacency list."""
    n = len(matrix)
    adj = {k: {} for k in range(n)}
    for k in range(n):
        for j in range(n):
            if matrix[k, j] != 0:
                adj[k][j] = {} if not etype else matrix[k, j]

    return adj