def copy(self, graph):
        
        """ Returns a copy of the layout for the given graph.
        """
        
        l = self.__class__(graph, self.n)
        l.i = 0
        return l