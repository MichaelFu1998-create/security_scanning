def get_edge_type(self, edge_type):
        """Returns all edges with the specified edge type.

        Parameters
        ----------
        edge_type : int
            An integer specifying what type of edges to return.

        Returns
        -------
        out : list of 2-tuples
            A list of 2-tuples representing the edges in the graph
            with the specified edge type.

        Examples
        --------
        Lets get type 2 edges from the following graph

        >>> import queueing_tool as qt
        >>> adjacency = {
        ...     0: {1: {'edge_type': 2}},
        ...     1: {2: {'edge_type': 1},
        ...         3: {'edge_type': 4}},
        ...     2: {0: {'edge_type': 2}},
        ...     3: {3: {'edge_type': 0}}
        ... }
        >>> G = qt.QueueNetworkDiGraph(adjacency)
        >>> ans = G.get_edge_type(2)
        >>> ans.sort()
        >>> ans
        [(0, 1), (2, 0)]
        """
        edges = []
        for e in self.edges():
            if self.adj[e[0]][e[1]].get('edge_type') == edge_type:
                edges.append(e)
        return edges