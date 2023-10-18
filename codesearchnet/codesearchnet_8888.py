def clear(self):
        """Clears out the queue. Removes all arrivals, departures, and
        queued agents from the :class:`.QueueServer`, resets
        ``num_arrivals``, ``num_departures``, ``num_system``, and the clock to
        zero. It also clears any stored ``data`` and the server is then
        set to inactive.
        """
        self.data = {}
        self._num_arrivals = 0
        self._oArrivals = 0
        self.num_departures = 0
        self.num_system = 0
        self._num_total = 0
        self._current_t = 0
        self._time = infty
        self._next_ct = 0
        self._active = False
        self.queue = collections.deque()
        inftyAgent = InftyAgent()
        self._arrivals = [inftyAgent]
        self._departures = [inftyAgent]