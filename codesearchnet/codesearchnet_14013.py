def crown(self, depth=2):
        """ Returns a list of leaves, nodes connected to leaves, etc.
        """
        nodes = []
        for node in self.leaves: nodes += node.flatten(depth-1)
        return cluster.unique(nodes)