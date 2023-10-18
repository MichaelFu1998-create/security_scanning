def get_gdb_response(
        self, timeout_sec=DEFAULT_GDB_TIMEOUT_SEC, raise_error_on_timeout=True
    ):
        """Get response from GDB, and block while doing so. If GDB does not have any response ready to be read
        by timeout_sec, an exception is raised.

        Args:
            timeout_sec (float): Maximum time to wait for reponse. Must be >= 0. Will return after
            raise_error_on_timeout (bool): Whether an exception should be raised if no response was found
            after timeout_sec

        Returns:
            List of parsed GDB responses, returned from gdbmiparser.parse_response, with the
            additional key 'stream' which is either 'stdout' or 'stderr'

        Raises:
            GdbTimeoutError if response is not received within timeout_sec
            ValueError if select returned unexpected file number
            NoGdbProcessError if there is no gdb subprocess running
        """

        self.verify_valid_gdb_subprocess()
        if timeout_sec < 0:
            self.logger.warning("timeout_sec was negative, replacing with 0")
            timeout_sec = 0

        if USING_WINDOWS:
            retval = self._get_responses_windows(timeout_sec)
        else:
            retval = self._get_responses_unix(timeout_sec)

        if not retval and raise_error_on_timeout:
            raise GdbTimeoutError(
                "Did not get response from gdb after %s seconds" % timeout_sec
            )

        else:
            return retval