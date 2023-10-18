def _sleep(self, seconds):
        """
        Sleep between requests, but don't force asynchronous code to wait

        :param seconds: The number of seconds to sleep
        :return: None
        """
        for _ in range(int(seconds)):
            if not self.force_stop:
                sleep(1)