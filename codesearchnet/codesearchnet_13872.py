def copy(self, graph):
        """ Returns a copy of all styles and a copy of the styleguide.
        """
        s = styles(graph)
        s.guide = self.guide.copy(graph)
        dict.__init__(s, [(v.name, v.copy()) for v in self.values()])
        return s