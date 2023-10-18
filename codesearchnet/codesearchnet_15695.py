def wait_until_final(self, poll_interval=1, timeout=60):
        """It will poll the URL to grab the latest status resource in a given
        timeout and time interval.

        Args:
            poll_interval (int): how often to poll the status service.
            timeout (int): how long to poll the URL until giving up. Use <= 0
                to wait forever

        """
        start_time = time.time()
        elapsed = 0
        while (self.status != "complete" and
                (timeout <= 0 or elapsed < timeout)):
            time.sleep(poll_interval)
            self.refresh()
            elapsed = time.time() - start_time