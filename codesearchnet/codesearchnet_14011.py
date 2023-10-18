def nodes_by_eigenvalue(self, treshold=0.0):
        """ Returns nodes sorted by eigenvector centrality.
        Nodes with a lot of incoming traffic will be at the front of the list
        """
        nodes = [(n.eigenvalue, n) for n in self.nodes if n.eigenvalue > treshold]
        nodes.sort(); nodes.reverse()
        return [n for w, n in nodes]