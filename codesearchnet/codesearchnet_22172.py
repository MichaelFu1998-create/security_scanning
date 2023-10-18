def connect_child(self, node):
        """Adds the given node as a child to this one.  No new nodes are
        created, only connections are made.
        
        :param node:
            a ``Node`` object to connect
        """
        if node.graph != self.graph:
            raise AttributeError('cannot connect nodes from different graphs')

        node.parents.add(self)
        self.children.add(node)