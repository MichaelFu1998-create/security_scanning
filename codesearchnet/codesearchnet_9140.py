def _dist(self, x, y, A):
        "(x - y)^T A (x - y)"
        return scipy.spatial.distance.mahalanobis(x, y, A) ** 2