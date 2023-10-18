def queue(self):
        """An ordered list of upcoming events.
        Events are named tuples with fields for:
            time, priority, action, arguments
        """
        # Use heapq to sort the queue rather than using 'sorted(self._queue)'.
        # With heapq, two events scheduled at the same time will show in
        # the actual order they would be retrieved.
        events = self._queue[:]
        return map(heapq.heappop, [events]*len(events))