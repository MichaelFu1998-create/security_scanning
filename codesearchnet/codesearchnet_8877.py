def desired_destination(self, network, edge):
        """Returns the agents next destination given their current
        location on the network.

        ``GreedyAgents`` choose their next destination with-in the
        network by picking the adjacent queue with the fewest number of
        :class:`Agents<.Agent>` in the queue.

        Parameters
        ----------
        network : :class:`.QueueNetwork`
            The :class:`.QueueNetwork` where the Agent resides.
        edge : tuple
            A 4-tuple indicating which edge this agent is located at.
            The first two slots indicate the current edge's source and
            target vertices, while the third slot indicates this edges
            ``edge_index``. The last slot indicates the edges edge
            type.

        Returns
        -------
        out : int
            Returns an the edge index corresponding to the agents next
            edge to visit in the network.
        """
        adjacent_edges = network.out_edges[edge[1]]
        d = _argmin([network.edge2queue[d].number_queued() for d in adjacent_edges])
        return adjacent_edges[d]