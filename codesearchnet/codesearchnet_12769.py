def node_radius(self, node):
        """
        Computes the radial position of the node.
        """
        return self.get_idx(node) * self.scale + self.internal_radius