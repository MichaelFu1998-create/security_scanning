def remove_random_edge(self):
        """Remove a random in-edge from the node with the lowest in/out degree ratio."""
        u, v, k = self.get_random_edge()
        log.log(5, 'removing %s, %s (%s)', u, v, k)
        self.graph.remove_edge(u, v, k)