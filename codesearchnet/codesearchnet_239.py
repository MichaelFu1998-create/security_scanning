def poll(self):
        """
        Get, and remove, the first (lowest) item from this queue.

        :return: the first (lowest) item from this queue.
        :rtype: Point, Event pair.
        """
        assert(len(self.events_scan) != 0)
        p, events_current = self.events_scan.pop_min()
        return p, events_current