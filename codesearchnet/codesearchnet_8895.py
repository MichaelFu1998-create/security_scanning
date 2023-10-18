def simulate(self, n=1, t=None, nA=None, nD=None):
        """This method simulates the queue forward for a specified
        amount of simulation time, or for a specific number of
        events.

        Parameters
        ----------
        n : int (optional, default: ``1``)
            The number of events to simulate. If ``t``, ``nA``, and
            ``nD`` are not given then this parameter is used.
        t : float (optional)
            The minimum amount of simulation time to simulate forward.
        nA : int (optional)
            Simulate until ``nA`` additional arrivals are observed.
        nD : int (optional)
            Simulate until ``nD`` additional departures are observed.

        Examples
        --------
        Before any simulations can take place the ``QueueServer`` must
        be activated:

        >>> import queueing_tool as qt
        >>> import numpy as np
        >>> rate = lambda t: 2 + 16 * np.sin(np.pi * t / 8)**2
        >>> arr = lambda t: qt.poisson_random_measure(t, rate, 18)
        >>> ser = lambda t: t + np.random.gamma(4, 0.1)
        >>> q = qt.QueueServer(5, arrival_f=arr, service_f=ser, seed=54)
        >>> q.set_active()

        To simulate 50000 events do the following:

        >>> q.simulate(50000)
        >>> num_events = q.num_arrivals[0] + q.num_departures
        >>> num_events
        50000

        To simulate forward 75 time units, do the following:

        >>> t0 = q.time
        >>> q.simulate(t=75)
        >>> round(float(q.time - t0), 1)
        75.1
        >>> q.num_arrivals[1] + q.num_departures - num_events
        1597

        To simulate forward until 1000 new departures are observed run:

        >>> nA0, nD0 = q.num_arrivals[1], q.num_departures
        >>> q.simulate(nD=1000)
        >>> q.num_departures - nD0, q.num_arrivals[1] - nA0
        (1000, 983)

        To simulate until 1000 new arrivals are observed run:

        >>> nA0, nD0 = q.num_arrivals[1], q.num_departures
        >>> q.simulate(nA=1000)
        >>> q.num_departures - nD0, q.num_arrivals[1] - nA0,
        (987, 1000)
        """
        if t is None and nD is None and nA is None:
            for dummy in range(n):
                self.next_event()
        elif t is not None:
            then = self._current_t + t
            while self._current_t < then and self._time < infty:
                self.next_event()
        elif nD is not None:
            num_departures = self.num_departures + nD
            while self.num_departures < num_departures and self._time < infty:
                self.next_event()
        elif nA is not None:
            num_arrivals = self._oArrivals + nA
            while self._oArrivals < num_arrivals and self._time < infty:
                self.next_event()