def _queueEvent(self, event, args):
        """Private method to queue events to run.

        Each event in queue is a tuple (event call, args to event call).
        """
        if not hasattr(self, 'eventList'):
            self.eventList = deque([(event, args)])
            return
        self.eventList.append((event, args))