def _postQueuedEvents(self, interval=0.01):
        """Private method to post queued events (e.g. Quartz events).

        Each event in queue is a tuple (event call, args to event call).
        """
        while len(self.eventList) > 0:
            (nextEvent, args) = self.eventList.popleft()
            nextEvent(*args)
            time.sleep(interval)