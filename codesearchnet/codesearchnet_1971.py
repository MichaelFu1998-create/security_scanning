def enterabs(self, time, priority, action, argument):
        """Enter a new event in the queue at an absolute time.
        Returns an ID for the event which can be used to remove it,
        if necessary.
        """
        event = Event(time, priority, action, argument)
        heapq.heappush(self._queue, event)
        return event