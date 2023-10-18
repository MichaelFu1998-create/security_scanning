def desired_destination(self, network, edge):
        """Returns the agents next destination given their current
        location on the network.

        An ``Agent`` chooses one of the out edges at random. The
        probability that the ``Agent`` will travel along a specific
        edge is specified in the :class:`QueueNetwork's<.QueueNetwork>`
        transition matrix.

        Parameters
        ----------
        network : :class:`.QueueNetwork`
            The :class:`.QueueNetwork` where the Agent resides.
        edge : tuple
            A 4-tuple indicating which edge this agent is located at.
            The first two slots indicate the current edge's source and
            target vertices, while the third slot indicates this edges
            ``edge_index``. The last slot indicates the edge type of
            that edge

        Returns
        -------
        out : int
            Returns an the edge index corresponding to the agents next
            edge to visit in the network.

        See Also
        --------
        :meth:`.transitions` : :class:`QueueNetwork's<.QueueNetwork>`
            method that returns the transition probabilities for each
            edge in the graph.
        """
        n = len(network.out_edges[edge[1]])
        if n <= 1:
            return network.out_edges[edge[1]][0]

        u = uniform()
        pr = network._route_probs[edge[1]]
        k = _choice(pr, u, n)

        # _choice returns an integer between 0 and n-1 where the
        # probability of k being selected is equal to pr[k].
        return network.out_edges[edge[1]][k]