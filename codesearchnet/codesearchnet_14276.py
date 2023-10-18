def copy(self, graph):
    
        """ Returns a copy of the event handler, remembering the last node clicked.
        """
    
        e = events(graph, self._ctx)
        e.clicked = self.clicked
        return e