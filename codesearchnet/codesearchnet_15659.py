def connect(self, blocking=False, retry=30):
        """
        Initiate connection to APRS server and attempt to login

        blocking = False     - Should we block until connected and logged-in
        retry = 30           - Retry interval in seconds
        """

        if self._connected:
            return

        while True:
            try:
                self._connect()
                if not self.skip_login:
                    self._send_login()
                break
            except (LoginError, ConnectionError):
                if not blocking:
                    raise

            self.logger.info("Retrying connection is %d seconds." % retry)
            time.sleep(retry)