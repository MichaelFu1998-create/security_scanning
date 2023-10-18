def add_edges(self):
        """
        Draws all of the edges in the graph.
        """
        for group, edgelist in self.edges.items():
            for (u, v, d) in edgelist:
                self.draw_edge(u, v, d, group)