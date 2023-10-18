def get_agent_data(self, queues=None, edge=None, edge_type=None, return_header=False):
        """Gets data from queues and organizes it by agent.

        If none of the parameters are given then data from every
        :class:`.QueueServer` is retrieved.

        Parameters
        ----------
        queues : int or *array_like* (optional)
            The edge index (or an iterable of edge indices) identifying
            the :class:`QueueServer(s)<.QueueServer>` whose data will
            be retrieved.
        edge : 2-tuple of int or *array_like* (optional)
            Explicitly specify which queues to retrieve agent data
            from. Must be either:

            * A 2-tuple of the edge's source and target vertex
              indices, or
            * An iterable of 2-tuples of the edge's source and
              target vertex indices.

        edge_type : int or an iterable of int (optional)
            A integer, or a collection of integers identifying which
            edge types to retrieve agent data from.
        return_header : bool (optonal, default: False)
            Determines whether the column headers are returned.

        Returns
        -------
        dict
            Returns a ``dict`` where the keys are the
            :class:`Agent's<.Agent>` ``agent_id`` and the values are
            :class:`ndarrays<~numpy.ndarray>` for that
            :class:`Agent's<.Agent>` data. The columns of this array
            are as follows:

            * First: The arrival time of an agent.
            * Second: The service start time of an agent.
            * Third: The departure time of an agent.
            * Fourth: The length of the queue upon the agents arrival.
            * Fifth: The total number of :class:`Agents<.Agent>` in the
              :class:`.QueueServer`.
            * Sixth: the :class:`QueueServer's<.QueueServer>` id
              (its edge index).

        headers : str (optional)
            A comma seperated string of the column headers. Returns
            ``'arrival,service,departure,num_queued,num_total,q_id'``
        """
        queues = _get_queues(self.g, queues, edge, edge_type)

        data = {}
        for qid in queues:
            for agent_id, dat in self.edge2queue[qid].data.items():
                datum = np.zeros((len(dat), 6))
                datum[:, :5] = np.array(dat)
                datum[:, 5] = qid
                if agent_id in data:
                    data[agent_id] = np.vstack((data[agent_id], datum))
                else:
                    data[agent_id] = datum

        dType = [
            ('a', float),
            ('s', float),
            ('d', float),
            ('q', float),
            ('n', float),
            ('id', float)
        ]
        for agent_id, dat in data.items():
            datum = np.array([tuple(d) for d in dat.tolist()], dtype=dType)
            datum = np.sort(datum, order='a')
            data[agent_id] = np.array([tuple(d) for d in datum])

        if return_header:
            return data, 'arrival,service,departure,num_queued,num_total,q_id'

        return data