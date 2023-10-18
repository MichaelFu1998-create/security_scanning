def _distance_matrix(self, a, b):
        """Pairwise distance between each point in `a` and each point in `b`"""
        def sq(x): return (x * x)
        # matrix = np.sum(map(lambda a,b: sq(a[:,None] - b[None,:]), a.T,
        #   b.T), axis=0)
        # A faster version than above:
        matrix = sq(a[:, 0][:, None] - b[:, 0][None, :])
        for x, y in zip(a.T[1:], b.T[1:]):
            matrix += sq(x[:, None] - y[None, :])
        return matrix