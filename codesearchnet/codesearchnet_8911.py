def start_collecting_data(self, queues=None, edge=None, edge_type=None):
        """Tells the queues to collect data on agents' arrival, service
        start, and departure times.

        If none of the parameters are given then every
        :class:`.QueueServer` will start collecting data.

        Parameters
        ----------
        queues : :any:`int`, *array_like* (optional)
            The edge index (or an iterable of edge indices) identifying
            the :class:`QueueServer(s)<.QueueServer>` that will start
            collecting data.
        edge : 2-tuple of int or *array_like* (optional)
            Explicitly specify which queues will collect data. Must be
            either:

            * A 2-tuple of the edge's source and target vertex
              indices, or
            * An iterable of 2-tuples of the edge's source and
              target vertex indices.

        edge_type : int or an iterable of int (optional)
            A integer, or a collection of integers identifying which
            edge types will be set active.
        """
        queues = _get_queues(self.g, queues, edge, edge_type)

        for k in queues:
            self.edge2queue[k].collect_data = True