def clear(self):
        """Resets the queue to its initial state.

        The attributes ``t``, ``num_events``, ``num_agents`` are set to
        zero, :meth:`.reset_colors` is called, and the
        :meth:`.QueueServer.clear` method is called for each queue in
        the network.

        Notes
        -----
        ``QueueNetwork`` must be re-initialized before any simulations
        can run.
        """
        self._t = 0
        self.num_events = 0
        self.num_agents = np.zeros(self.nE, int)
        self._fancy_heap = PriorityQueue()
        self._prev_edge = None
        self._initialized = False
        self.reset_colors()
        for q in self.edge2queue:
            q.clear()