def clear_data(self, queues=None, edge=None, edge_type=None):
        """Clears data from all queues.

        If none of the parameters are given then every queue's data is
        cleared.

        Parameters
        ----------
        queues : int or an iterable of int (optional)
            The edge index (or an iterable of edge indices) identifying
            the :class:`QueueServer(s)<.QueueServer>` whose data will
            be cleared.
        edge : 2-tuple of int or *array_like* (optional)
            Explicitly specify which queues' data to clear. Must be
            either:

            * A 2-tuple of the edge's source and target vertex
              indices, or
            * An iterable of 2-tuples of the edge's source and
              target vertex indices.

        edge_type : int or an iterable of int (optional)
            A integer, or a collection of integers identifying which
            edge types will have their data cleared.
        """
        queues = _get_queues(self.g, queues, edge, edge_type)

        for k in queues:
            self.edge2queue[k].data = {}