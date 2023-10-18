def _poll_read(self, expected, timeout_s=5.0):
        """Helper function to continuously poll reads on the FTDI device until an
        expected number of bytes are returned.  Will throw a timeout error if no
        data is received within the specified number of timeout seconds.  Returns
        the read data as a string if successful, otherwise raises an execption.
        """
        start = time.time()
        # Start with an empty response buffer.
        response = bytearray(expected)
        index = 0
        # Loop calling read until the response buffer is full or a timeout occurs.
        while time.time() - start <= timeout_s:
            ret, data = ftdi.read_data(self._ctx, expected - index)
            # Fail if there was an error reading data.
            if ret < 0:
                raise RuntimeError('ftdi_read_data failed with error code {0}.'.format(ret))
            # Add returned data to the buffer.
            response[index:index+ret] = data[:ret]
            index += ret
            # Buffer is full, return the result data.
            if index >= expected:
                return str(response)
            time.sleep(0.01)
        raise RuntimeError('Timeout while polling ftdi_read_data for {0} bytes!'.format(expected))