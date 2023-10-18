def node_theta(self, node):
        """
        Convenience function to find the node's theta angle.
        """
        group = self.find_node_group_membership(node)
        return self.group_theta(group)