def show_type(self, edge_type, **kwargs):
        """Draws the network, highlighting queues of a certain type.

        The colored vertices represent self loops of type ``edge_type``.
        Dark edges represent queues of type ``edge_type``.

        Parameters
        ----------
        edge_type : int
            The type of vertices and edges to be shown.
        **kwargs
            Any additional parameters to pass to :meth:`.draw`, and
            :meth:`.QueueNetworkDiGraph.draw_graph`

        Notes
        -----
        The colors are defined by the class attribute ``colors``. The
        relevant colors are ``vertex_active``, ``vertex_inactive``,
        ``vertex_highlight``, ``edge_active``, and ``edge_inactive``.

        Examples
        --------
        The following code highlights all edges with edge type ``2``.
        If the edge is a loop then the vertex is highlighted as well.
        In this case all edges with edge type ``2`` happen to be loops.

        >>> import queueing_tool as qt
        >>> g = qt.generate_pagerank_graph(100, seed=13)
        >>> net = qt.QueueNetwork(g, seed=13)
        >>> fname = 'edge_type_2.png'
        >>> net.show_type(2, fname=fname) # doctest: +SKIP

        .. figure:: edge_type_2-1.png
           :align: center
        """
        for v in self.g.nodes():
            e = (v, v)
            if self.g.is_edge(e) and self.g.ep(e, 'edge_type') == edge_type:
                ei = self.g.edge_index[e]
                self.g.set_vp(v, 'vertex_fill_color', self.colors['vertex_highlight'])
                self.g.set_vp(v, 'vertex_color', self.edge2queue[ei].colors['vertex_color'])
            else:
                self.g.set_vp(v, 'vertex_fill_color', self.colors['vertex_inactive'])
                self.g.set_vp(v, 'vertex_color', [0, 0, 0, 0.9])

        for e in self.g.edges():
            if self.g.ep(e, 'edge_type') == edge_type:
                self.g.set_ep(e, 'edge_color', self.colors['edge_active'])
            else:
                self.g.set_ep(e, 'edge_color', self.colors['edge_inactive'])

        self.draw(update_colors=False, **kwargs)
        self._update_all_colors()