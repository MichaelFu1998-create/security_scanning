def next_event_description(self):
        """Returns whether the next event is an arrival or a departure
        and the queue the event is accuring at.

        Returns
        -------
        des : str
            Indicates whether the next event is an arrival, a
            departure, or nothing; returns ``'Arrival'``,
            ``'Departure'``, or ``'Nothing'``.
        edge : int or ``None``
            The edge index of the edge that this event will occur at.
            If there are no events then ``None`` is returned.
        """
        if self._fancy_heap.size == 0:
            event_type = 'Nothing'
            edge_index = None
        else:
            s = [q._key() for q in self.edge2queue]
            s.sort()
            e = s[0][1]
            q = self.edge2queue[e]

            event_type = 'Arrival' if q.next_event_description() == 1 else 'Departure'
            edge_index = q.edge[2]
        return event_type, edge_index