def betweenness_centrality(self, normalized=True):
        """ Calculates betweenness centrality and returns an node id -> weight dictionary.
        Node betweenness weights are updated in the process.
        """
        bc = proximity.brandes_betweenness_centrality(self, normalized)
        for id, w in bc.iteritems(): self[id]._betweenness = w
        return bc