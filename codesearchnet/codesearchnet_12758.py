def simplified_edges(self):
        """
        A generator for getting all of the edges without consuming extra
        memory.
        """
        for group, edgelist in self.edges.items():
            for u, v, d in edgelist:
                yield (u, v)