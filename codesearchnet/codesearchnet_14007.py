def prune(self, depth=0):
        """ Removes all nodes with less or equal links than depth.
        """
        for n in list(self.nodes):
            if len(n.links) <= depth:
                self.remove_node(n.id)