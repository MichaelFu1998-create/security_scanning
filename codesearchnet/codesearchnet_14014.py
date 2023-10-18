def _density(self):
        """ The number of edges in relation to the total number of possible edges.
        """
        return 2.0*len(self.edges) / (len(self.nodes) * (len(self.nodes)-1))