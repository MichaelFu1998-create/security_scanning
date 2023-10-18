def get_queue_data(self, queues=None, edge=None, edge_type=None, return_header=False):
        """Gets data from all the queues.

        If none of the parameters are given then data from every
        :class:`.QueueServer` is retrieved.

        Parameters
        ----------
        queues : int or an *array_like* of int, (optional)
            The edge index (or an iterable of edge indices) identifying
            the :class:`QueueServer(s)<.QueueServer>` whose data will
            be retrieved.
        edge : 2-tuple of int or *array_like* (optional)
            Explicitly specify which queues to retrieve data from. Must
            be either:

            * A 2-tuple of the edge's source and target vertex
              indices, or
            * An iterable of 2-tuples of the edge's source and
              target vertex indices.

        edge_type : int or an iterable of int (optional)
            A integer, or a collection of integers identifying which
            edge types to retrieve data from.
        return_header : bool (optonal, default: False)
            Determines whether the column headers are returned.

        Returns
        -------
        out : :class:`~numpy.ndarray`
            * 1st: The arrival time of an agent.
            * 2nd: The service start time of an agent.
            * 3rd: The departure time of an agent.
            * 4th: The length of the queue upon the agents arrival.
            * 5th: The total number of :class:`Agents<.Agent>` in the
              :class:`.QueueServer`.
            * 6th: The :class:`QueueServer's<.QueueServer>` edge index.

        out : str (optional)
            A comma seperated string of the column headers. Returns
            ``'arrival,service,departure,num_queued,num_total,q_id'```

        Examples
        --------
        Data is not collected by default. Before simulating, by sure to
        turn it on (as well as initialize the network). The following
        returns data from queues with ``edge_type`` 1 or 3:

        >>> import queueing_tool as qt
        >>> g = qt.generate_pagerank_graph(100, seed=13)
        >>> net = qt.QueueNetwork(g, seed=13)
        >>> net.start_collecting_data()
        >>> net.initialize(10)
        >>> net.simulate(2000)
        >>> data = net.get_queue_data(edge_type=(1, 3))

        To get data from an edge connecting two vertices do the
        following:

        >>> data = net.get_queue_data(edge=(1, 50))

        To get data from several edges do the following:

        >>> data = net.get_queue_data(edge=[(1, 50), (10, 91), (99, 99)])

        You can specify the edge indices as well:

        >>> data = net.get_queue_data(queues=(20, 14, 0, 4))
        """
        queues = _get_queues(self.g, queues, edge, edge_type)

        data = np.zeros((0, 6))
        for q in queues:
            dat = self.edge2queue[q].fetch_data()

            if len(dat) > 0:
                data = np.vstack((data, dat))

        if return_header:
            return data, 'arrival,service,departure,num_queued,num_total,q_id'

        return data