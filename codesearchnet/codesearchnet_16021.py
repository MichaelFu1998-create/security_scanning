def node(self, node):
        """
        Return the other node
        """

        if node == self.node1:
            return self.node2
        elif node == self.node2:
            return self.node1
        else:
            return None