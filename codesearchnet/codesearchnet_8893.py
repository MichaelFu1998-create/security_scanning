def next_event_description(self):
        """Returns an integer representing whether the next event is
        an arrival, a departure, or nothing.

        Returns
        -------
        out : int
            An integer representing whether the next event is an
            arrival or a departure: ``1`` corresponds to an arrival,
            ``2`` corresponds to a departure, and ``0`` corresponds to
            nothing scheduled to occur.
        """
        if self._departures[0]._time < self._arrivals[0]._time:
            return 2
        elif self._arrivals[0]._time < infty:
            return 1
        else:
            return 0