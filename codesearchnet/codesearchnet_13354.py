def check_events(self):
        """Call the event dispatcher.

        Quit the main loop when the `QUIT` event is reached.

        :Return: `True` if `QUIT` was reached.
        """
        if self.event_dispatcher.flush() is QUIT:
            self._quit = True
            return True
        return False