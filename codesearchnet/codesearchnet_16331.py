def pm(self):
        """Read the PM data and reset the histogram

        **NOTE: This method is supported by firmware v18+.**

        :rtype: dictionary

        :Example:

        >>> alpha.pm()
        {
            'PM1': 0.12,
            'PM2.5': 0.24,
            'PM10': 1.42
        }
        """

        resp = []
        data = {}

        # Send the command byte
        self.cnxn.xfer([0x32])

        # Wait 10 ms
        sleep(10e-3)

        # read the histogram
        for i in range(12):
            r = self.cnxn.xfer([0x00])[0]
            resp.append(r)

        # convert to real things and store in dictionary!
        data['PM1']     = self._calculate_float(resp[0:4])
        data['PM2.5']   = self._calculate_float(resp[4:8])
        data['PM10']    = self._calculate_float(resp[8:])

        sleep(0.1)

        return data