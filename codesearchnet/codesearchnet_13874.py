def copy(self, graph):
        """ Returns a copy of the styleguide for the given graph.
        """
        g = styleguide(graph)
        g.order = self.order
        dict.__init__(g, [(k, v) for k, v in self.iteritems()])
        return g