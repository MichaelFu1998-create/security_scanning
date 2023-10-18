def show_active(self, **kwargs):
        """Draws the network, highlighting active queues.

        The colored vertices represent vertices that have at least one
        queue on an in-edge that is active. Dark edges represent
        queues that are active, light edges represent queues that are
        inactive.

        Parameters
        ----------
        **kwargs
            Any additional parameters to pass to :meth:`.draw`, and
            :meth:`.QueueNetworkDiGraph.draw_graph`.

        Notes
        -----
        Active queues are :class:`QueueServers<.QueueServer>` that
        accept arrivals from outside the network. The colors are
        defined by the class attribute ``colors``. The relevant keys
        are ``vertex_active``, ``vertex_inactive``, ``edge_active``,
        and ``edge_inactive``.
        """
        g = self.g
        for v in g.nodes():
            self.g.set_vp(v, 'vertex_color', [0, 0, 0, 0.9])
            is_active = False
            my_iter = g.in_edges(v) if g.is_directed() else g.out_edges(v)
            for e in my_iter:
                ei = g.edge_index[e]
                if self.edge2queue[ei]._active:
                    is_active = True
                    break
            if is_active:
                self.g.set_vp(v, 'vertex_fill_color', self.colors['vertex_active'])
            else:
                self.g.set_vp(v, 'vertex_fill_color', self.colors['vertex_inactive'])

        for e in g.edges():
            ei = g.edge_index[e]
            if self.edge2queue[ei]._active:
                self.g.set_ep(e, 'edge_color', self.colors['edge_active'])
            else:
                self.g.set_ep(e, 'edge_color', self.colors['edge_inactive'])

        self.draw(update_colors=False, **kwargs)
        self._update_all_colors()