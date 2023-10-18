def nodes_by_betweenness(self, treshold=0.0):
        """ Returns nodes sorted by betweenness centrality.
        Nodes with a lot of passing traffic will be at the front of the list.
        """
        nodes = [(n.betweenness, n) for n in self.nodes if n.betweenness > treshold]
        nodes.sort(); nodes.reverse()
        return [n for w, n in nodes]