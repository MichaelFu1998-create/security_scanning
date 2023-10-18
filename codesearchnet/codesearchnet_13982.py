def call_bad_cb(self, tb):
        """
        If bad_cb returns True then keep it
        :param tb: traceback that caused exception
        :return:
        """
        with LiveExecution.lock:
            if self.bad_cb and not self.bad_cb(tb):
                self.bad_cb = None