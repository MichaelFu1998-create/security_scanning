def can_reach(self, node, traversable=lambda node, edge: True):
        
        """ Returns True if given node can be reached over traversable edges.
        To enforce edge direction, use a node==edge.node1 traversable.
        """
        
        if isinstance(node, str):
            node = self.graph[node]
        for n in self.graph.nodes:
            n._visited = False
        return proximity.depth_first_search(self,
            visit=lambda n: node == n,
            traversable=traversable
            )