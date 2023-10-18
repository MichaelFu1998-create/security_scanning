def read_firmware(self):
        """Read the firmware version of the OPC-N2. Firmware v18+ only.

        :rtype: dict

        :Example:

        >>> alpha.read_firmware()
        {
            'major': 18,
            'minor': 2,
            'version': 18.2
        }
        """
        # Send the command byte and sleep for 9 ms
        self.cnxn.xfer([0x12])
        sleep(10e-3)

        self.firmware['major'] = self.cnxn.xfer([0x00])[0]
        self.firmware['minor'] = self.cnxn.xfer([0x00])[0]

        # Build the firmware version
        self.firmware['version'] = float('{}.{}'.format(self.firmware['major'], self.firmware['minor']))

        sleep(0.1)

        return self.firmware