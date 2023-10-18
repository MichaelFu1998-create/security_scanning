def reset_counter(self):
        """ reset the failed connection counters
        """
        self._cnt_retries = 0
        for i in self._url_counter:
            self._url_counter[i] = 0