def read_bin_boundaries(self):
        """Return the bin boundaries.

        :returns: dictionary with 17 bin boundaries.
        """
        config  = []
        data    = {}

        # Send the command byte and sleep for 10 ms
        self.cnxn.xfer([0x33])
        sleep(10e-3)

        # Read the config variables by sending 256 empty bytes
        for i in range(30):
            resp = self.cnxn.xfer([0x00])[0]
            config.append(resp)

        # Add the bin bounds to the dictionary of data [bytes 0-29]
        for i in range(0, 14):
            data["Bin Boundary {0}".format(i)] = self._16bit_unsigned(config[2*i], config[2*i + 1])

        return data