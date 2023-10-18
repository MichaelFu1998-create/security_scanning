def call_good_cb(self):
        """
        If good_cb returns True then keep it
        :return:
        """
        with LiveExecution.lock:
            if self.good_cb and not self.good_cb():
                self.good_cb = None