def _frame_limit(self, start_time):
        """
        Limit to framerate, should be called after
        rendering has completed

        :param start_time: When execution started
        """
        if self._speed:
            completion_time = time()
            exc_time = completion_time - start_time
            sleep_for = (1.0 / abs(self._speed)) - exc_time
            if sleep_for > 0:
                sleep(sleep_for)