def flush(self, dispatch = True):
        """Read all events currently in the queue and dispatch them to the
        handlers unless `dispatch` is `False`.

        Note: If the queue contains `QUIT` the events after it won't be
        removed.

        :Parameters:
            - `dispatch`: if the events should be handled (`True`) or ignored
              (`False`)

        :Return: `QUIT` if the `QUIT` event was reached.
        """
        if dispatch:
            while True:
                event = self.dispatch(False)
                if event in (None, QUIT):
                    return event
        else:
            while True:
                try:
                    self.queue.get(False)
                except Queue.Empty:
                    return None