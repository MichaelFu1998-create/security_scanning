def click(self, node):
        
        """ Callback from graph.events when a node is clicked.
        """
        
        if not self.has_node(node.id): return
        if node == self.root: return
        
        self._dx, self._dy = self.offset(node)
        self.previous = self.root.id
        self.load(node.id)