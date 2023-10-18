def read_pot_status(self):
        """Read the status of the digital pot. Firmware v18+ only.
        The return value is a dictionary containing the following as
        unsigned 8-bit integers: FanON, LaserON, FanDACVal, LaserDACVal.

        :rtype: dict

        :Example:

        >>> alpha.read_pot_status()
        {
            'LaserDACVal': 230,
            'FanDACVal': 255,
            'FanON': 0,
            'LaserON': 0
        }
        """
        # Send the command byte and wait 10 ms
        a = self.cnxn.xfer([0x13])[0]

        sleep(10e-3)

        # Build an array of the results
        res = []
        for i in range(4):
            res.append(self.cnxn.xfer([0x00])[0])

        sleep(0.1)

        return {
            'FanON':        res[0],
            'LaserON':      res[1],
            'FanDACVal':    res[2],
            'LaserDACVal':  res[3]
            }