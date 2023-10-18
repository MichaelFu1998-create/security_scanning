def delay_service(self, t=None):
        """Adds an extra service time to the next departing
        :class:`Agent's<.Agent>` service time.

        Parameters
        ----------
        t : float (optional)
            Specifies the departing time for the agent scheduled
            to depart next. If ``t`` is not given, then an additional
            service time is added to the next departing agent.
        """
        if len(self._departures) > 1:
            agent = heappop(self._departures)

            if t is None:
                agent._time = self.service_f(agent._time)
            else:
                agent._time = t

            heappush(self._departures, agent)
            self._update_time()