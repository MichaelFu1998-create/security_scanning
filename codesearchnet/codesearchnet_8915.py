def next_event(self):
        """Simulates the queue forward one event.

        This method behaves identically to a :class:`.LossQueue` if the
        arriving/departing agent is anything other than a
        :class:`.ResourceAgent`. The differences are;

        Arriving:

        * If the :class:`.ResourceAgent` has a resource then it deletes
          the agent upon arrival and adds one to ``num_servers``.
        * If the :class:`.ResourceAgent` is arriving without a resource
          then nothing special happens.

        Departing:

        * If the :class:`.ResourceAgent` does not have a resource, then
          ``num_servers`` decreases by one and the agent then *has a
          resource*.

        Use :meth:`~QueueServer.simulate` for simulating instead.
        """
        if isinstance(self._arrivals[0], ResourceAgent):
            if self._departures[0]._time < self._arrivals[0]._time:
                return super(ResourceQueue, self).next_event()
            elif self._arrivals[0]._time < infty:
                if self._arrivals[0]._has_resource:
                    arrival = heappop(self._arrivals)
                    self._current_t = arrival._time
                    self._num_total -= 1
                    self.set_num_servers(self.num_servers + 1)

                    if self.collect_data:
                        t = arrival._time
                        if arrival.agent_id not in self.data:
                            self.data[arrival.agent_id] = [[t, t, t, len(self.queue), self.num_system]]
                        else:
                            self.data[arrival.agent_id].append([t, t, t, len(self.queue), self.num_system])

                    if self._arrivals[0]._time < self._departures[0]._time:
                        self._time = self._arrivals[0]._time
                    else:
                        self._time = self._departures[0]._time

                elif self.num_system < self.num_servers:
                    super(ResourceQueue, self).next_event()

                else:
                    self.num_blocked += 1
                    self._num_arrivals += 1
                    self._num_total -= 1
                    arrival = heappop(self._arrivals)
                    self._current_t = arrival._time

                    if self.collect_data:
                        if arrival.agent_id not in self.data:
                            self.data[arrival.agent_id] = [[arrival._time, 0, 0, len(self.queue), self.num_system]]
                        else:
                            self.data[arrival.agent_id].append([arrival._time, 0, 0, len(self.queue), self.num_system])

                    if self._arrivals[0]._time < self._departures[0]._time:
                        self._time = self._arrivals[0]._time
                    else:
                        self._time = self._departures[0]._time
        else:
            return super(ResourceQueue, self).next_event()