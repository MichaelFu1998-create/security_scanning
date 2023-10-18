def _write(self, string):
        """Helper function to call write_data on the provided FTDI device and
        verify it succeeds.
        """
        # Get modem status. Useful to enable for debugging.
        #ret, status = ftdi.poll_modem_status(self._ctx)
        #if ret == 0:
        #	logger.debug('Modem status {0:02X}'.format(status))
        #else:
        #	logger.debug('Modem status error {0}'.format(ret))
        length = len(string)
        try:
            ret = ftdi.write_data(self._ctx, string, length)
        except TypeError:
            ret = ftdi.write_data(self._ctx, string); #compatible with libFtdi 1.3
        # Log the string that was written in a python hex string format using a very
        # ugly one-liner list comprehension for brevity.
        #logger.debug('Wrote {0}'.format(''.join(['\\x{0:02X}'.format(ord(x)) for x in string])))
        if ret < 0:
            raise RuntimeError('ftdi_write_data failed with error {0}: {1}'.format(ret, ftdi.get_error_string(self._ctx)))
        if ret != length:
            raise RuntimeError('ftdi_write_data expected to write {0} bytes but actually wrote {1}!'.format(length, ret))