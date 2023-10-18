def config2(self):
        """Read the second set of configuration variables and return as a dictionary.

        **NOTE: This method is supported by firmware v18+.**

        :rtype: dictionary

        :Example:

        >>> a.config2()
        {
            'AMFanOnIdle': 0,
            'AMIdleIntervalCount': 0,
            'AMMaxDataArraysInFile': 61798,
            'AMSamplingInterval': 1,
            'AMOnlySavePMData': 0,
            'AMLaserOnIdle': 0
        }
        """
        config  = []
        data    = {}

        # Send the command byte and sleep for 10 ms
        self.cnxn.xfer([0x3D])
        sleep(10e-3)

        # Read the config variables by sending 256 empty bytes
        for i in range(9):
            resp = self.cnxn.xfer([0x00])[0]
            config.append(resp)

        data["AMSamplingInterval"]      = self._16bit_unsigned(config[0], config[1])
        data["AMIdleIntervalCount"]     = self._16bit_unsigned(config[2], config[3])
        data['AMFanOnIdle']             = config[4]
        data['AMLaserOnIdle']           = config[5]
        data['AMMaxDataArraysInFile']   = self._16bit_unsigned(config[6], config[7])
        data['AMOnlySavePMData']        = config[8]

        sleep(0.1)

        return data