def transitions(self, return_matrix=True):
        """Returns the routing probabilities for each vertex in the
        graph.

        Parameters
        ----------
        return_matrix : bool (optional, the default is ``True``)
            Specifies whether an :class:`~numpy.ndarray` is returned.
            If ``False``, a dict is returned instead.

        Returns
        -------
        out : a dict or :class:`~numpy.ndarray`
            The transition probabilities for each vertex in the graph.
            If ``out`` is an :class:`~numpy.ndarray`, then
            ``out[v, u]`` returns the probability of a transition from
            vertex ``v`` to vertex ``u``. If ``out`` is a dict
            then ``out_edge[v][u]`` is the probability of moving from
            vertex ``v`` to the vertex ``u``.

        Examples
        --------
        Lets change the routing probabilities:

        >>> import queueing_tool as qt
        >>> import networkx as nx
        >>> g = nx.sedgewick_maze_graph()
        >>> net = qt.QueueNetwork(g)

        Below is an adjacency list for the graph ``g``.

        >>> ans = qt.graph2dict(g, False)
        >>> {k: sorted(v) for k, v in ans.items()}
        ...                         # doctest: +NORMALIZE_WHITESPACE
        {0: [2, 5, 7],
         1: [7],
         2: [0, 6],
         3: [4, 5],
         4: [3, 5, 6, 7],
         5: [0, 3, 4],
         6: [2, 4],
         7: [0, 1, 4]}

        The default transition matrix is every out edge being equally
        likely:

        >>> net.transitions(False)  # doctest: +ELLIPSIS
        ...                         # doctest: +NORMALIZE_WHITESPACE
        {0: {2: 0.333..., 5: 0.333..., 7: 0.333...},
         1: {7: 1.0},
         2: {0: 0.5, 6: 0.5},
         3: {4: 0.5, 5: 0.5},
         4: {3: 0.25, 5: 0.25, 6: 0.25, 7: 0.25},
         5: {0: 0.333..., 3: 0.333..., 4: 0.333...},
         6: {2: 0.5, 4: 0.5},
         7: {0: 0.333..., 1: 0.333..., 4: 0.333...}}

        Now we will generate a random routing matrix:

        >>> mat = qt.generate_transition_matrix(g, seed=96)
        >>> net.set_transitions(mat)
        >>> net.transitions(False)  # doctest: +ELLIPSIS
        ...                         # doctest: +NORMALIZE_WHITESPACE
        {0: {2: 0.112..., 5: 0.466..., 7: 0.420...},
         1: {7: 1.0},
         2: {0: 0.561..., 6: 0.438...},
         3: {4: 0.545..., 5: 0.454...},
         4: {3: 0.374..., 5: 0.381..., 6: 0.026..., 7: 0.217...},
         5: {0: 0.265..., 3: 0.460..., 4: 0.274...},
         6: {2: 0.673..., 4: 0.326...},
         7: {0: 0.033..., 1: 0.336..., 4: 0.630...}}

        What this shows is the following: when an :class:`.Agent` is at
        vertex ``2`` they will transition to vertex ``0`` with
        probability ``0.561`` and route to vertex ``6`` probability
        ``0.438``, when at vertex ``6`` they will transition back to
        vertex ``2`` with probability ``0.673`` and route vertex ``4``
        probability ``0.326``, etc.
        """
        if return_matrix:
            mat = np.zeros((self.nV, self.nV))
            for v in self.g.nodes():
                ind = [e[1] for e in sorted(self.g.out_edges(v))]
                mat[v, ind] = self._route_probs[v]
        else:
            mat = {
                k: {e[1]: p for e, p in zip(sorted(self.g.out_edges(k)), value)}
                for k, value in enumerate(self._route_probs)
            }

        return mat