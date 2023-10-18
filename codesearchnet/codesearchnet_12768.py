def get_idx(self, node):
        """
        Finds the index of the node in the sorted list.
        """
        group = self.find_node_group_membership(node)
        return self.nodes[group].index(node)