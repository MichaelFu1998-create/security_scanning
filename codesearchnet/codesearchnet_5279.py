def _check(self, command, *args):
        """Helper function to call the provided command on the FTDI device and
        verify the response matches the expected value.
        """
        ret = command(self._ctx, *args)
        logger.debug('Called ftdi_{0} and got response {1}.'.format(command.__name__, ret))
        if ret != 0:
            raise RuntimeError('ftdi_{0} failed with error {1}: {2}'.format(command.__name__, ret, ftdi.get_error_string(self._ctx)))