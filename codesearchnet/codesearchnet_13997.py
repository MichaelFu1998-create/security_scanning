def copy(self, empty=False):
        
        """ Create a copy of the graph (by default with nodes and edges).
        """
        
        g = graph(self.layout.n, self.distance, self.layout.type)
        g.layout = self.layout.copy(g)
        g.styles = self.styles.copy(g)
        g.events = self.events.copy(g)

        if not empty:
            for n in self.nodes:
                g.add_node(n.id, n.r, n.style, n.category, n.label, (n == self.root), n.__dict__)
            for e in self.edges:
                g.add_edge(e.node1.id, e.node2.id, e.weight, e.length, e.label, e.__dict__)
        
        return g