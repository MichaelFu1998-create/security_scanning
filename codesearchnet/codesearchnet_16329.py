def sn(self):
        """Read the Serial Number string. This method is only available on OPC-N2
        firmware versions 18+.

        :rtype: string

        :Example:

        >>> alpha.sn()
        'OPC-N2 123456789'
        """
        string = []

        # Send the command byte and sleep for 9 ms
        self.cnxn.xfer([0x10])
        sleep(9e-3)

        # Read the info string by sending 60 empty bytes
        for i in range(60):
            resp = self.cnxn.xfer([0x00])[0]
            string.append(chr(resp))

        sleep(0.1)

        return ''.join(string)