def eigenvector_centrality(self, normalized=True, reversed=True, rating={},
                               start=None, iterations=100, tolerance=0.0001):
        """ Calculates eigenvector centrality and returns an node id -> weight dictionary.
        Node eigenvalue weights are updated in the process.
        """
        ec = proximity.eigenvector_centrality(
            self, normalized, reversed, rating, start, iterations, tolerance
        )
        for id, w in ec.iteritems(): self[id]._eigenvalue = w
        return ec