def simulate(self, n=1, t=None):
        """Simulates the network forward.

        Simulates either a specific number of events or for a specified
        amount of simulation time.

        Parameters
        ----------
        n : int (optional, default: 1)
            The number of events to simulate. If ``t`` is not given
            then this parameter is used.
        t : float (optional)
            The amount of simulation time to simulate forward. If
            given, ``t`` is used instead of ``n``.

        Raises
        ------
        QueueingToolError
            Will raise a :exc:`.QueueingToolError` if the
            ``QueueNetwork`` has not been initialized. Call
            :meth:`.initialize` before calling this method.

        Examples
        --------
        Let ``net`` denote your instance of a ``QueueNetwork``. Before
        you simulate, you need to initialize the network, which allows
        arrivals from outside the network. To initialize with 2 (random
        chosen) edges accepting arrivals run:

        >>> import queueing_tool as qt
        >>> g = qt.generate_pagerank_graph(100, seed=50)
        >>> net = qt.QueueNetwork(g, seed=50)
        >>> net.initialize(2)

        To simulate the network 50000 events run:

        >>> net.num_events
        0
        >>> net.simulate(50000)
        >>> net.num_events
        50000

        To simulate the network for at least 75 simulation time units
        run:

        >>> t0 = net.current_time
        >>> net.simulate(t=75)
        >>> t1 = net.current_time
        >>> t1 - t0 # doctest: +ELLIPSIS
        75...
        """
        if not self._initialized:
            msg = ("Network has not been initialized. "
                   "Call '.initialize()' first.")
            raise QueueingToolError(msg)
        if t is None:
            for dummy in range(n):
                self._simulate_next_event(slow=False)
        else:
            now = self._t
            while self._t < now + t:
                self._simulate_next_event(slow=False)