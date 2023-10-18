def _sm_cleanup(self, *args, **kwargs):
        """
        Delete all state associated with the chaos session
        """
        if self._done_notification_func is not None:
            self._done_notification_func()
        self._timer.cancel()