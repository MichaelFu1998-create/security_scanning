def initialize(self, nActive=1, queues=None, edges=None, edge_type=None):
        """Prepares the ``QueueNetwork`` for simulation.

        Each :class:`.QueueServer` in the network starts inactive,
        which means they do not accept arrivals from outside the
        network, and they have no agents in their system. This method
        sets queues to active, which then allows agents to arrive from
        outside the network.

        Parameters
        ----------
        nActive : int (optional, default: ``1``)
            The number of queues to set as active. The queues are
            selected randomly.
        queues : int *array_like* (optional)
            The edge index (or an iterable of edge indices) identifying
            the :class:`QueueServer(s)<.QueueServer>` to make active by.
        edges : 2-tuple of int or *array_like* (optional)
            Explicitly specify which queues to make active. Must be
            either:

            * A 2-tuple of the edge's source and target vertex
              indices, or
            * An iterable of 2-tuples of the edge's source and
              target vertex indices.

        edge_type : int or an iterable of int (optional)
            A integer, or a collection of integers identifying which
            edge types will be set active.

        Raises
        ------
        ValueError
            If ``queues``, ``egdes``, and ``edge_type`` are all ``None``
            and ``nActive`` is an integer less than 1
            :exc:`~ValueError` is raised.
        TypeError
            If ``queues``, ``egdes``, and ``edge_type`` are all ``None``
            and ``nActive`` is not an integer then a :exc:`~TypeError`
            is raised.
        QueueingToolError
            Raised if all the queues specified are
            :class:`NullQueues<.NullQueue>`.

        Notes
        -----
        :class:`NullQueues<.NullQueue>` cannot be activated, and are
        sifted out if they are specified. More specifically, every edge
        with edge type 0 is sifted out.
        """
        if queues is None and edges is None and edge_type is None:
            if nActive >= 1 and isinstance(nActive, numbers.Integral):
                qs = [q.edge[2] for q in self.edge2queue if q.edge[3] != 0]
                n = min(nActive, len(qs))
                queues = np.random.choice(qs, size=n, replace=False)
            elif not isinstance(nActive, numbers.Integral):
                msg = "If queues is None, then nActive must be an integer."
                raise TypeError(msg)
            else:
                msg = ("If queues is None, then nActive must be a "
                       "positive int.")
                raise ValueError(msg)
        else:
            queues = _get_queues(self.g, queues, edges, edge_type)

        queues = [e for e in queues if self.edge2queue[e].edge[3] != 0]

        if len(queues) == 0:
            raise QueueingToolError("There were no queues to initialize.")

        if len(queues) > self.max_agents:
            queues = queues[:self.max_agents]

        for ei in queues:
            self.edge2queue[ei].set_active()
            self.num_agents[ei] = self.edge2queue[ei]._num_total

        keys = [q._key() for q in self.edge2queue if q._time < np.infty]
        self._fancy_heap = PriorityQueue(keys, self.nE)
        self._initialized = True