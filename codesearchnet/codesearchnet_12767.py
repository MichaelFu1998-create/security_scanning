def find_node_group_membership(self, node):
        """
        Identifies the group for which a node belongs to.
        """
        for group, nodelist in self.nodes.items():
            if node in nodelist:
                return group