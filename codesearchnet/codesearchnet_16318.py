def read_info_string(self):
        """Reads the information string for the OPC

        :rtype: string

        :Example:

        >>> alpha.read_info_string()
        'OPC-N2 FirmwareVer=OPC-018.2....................BD'
        """
        infostring = []

        # Send the command byte and sleep for 9 ms
        self.cnxn.xfer([0x3F])
        sleep(9e-3)

        # Read the info string by sending 60 empty bytes
        for i in range(60):
            resp = self.cnxn.xfer([0x00])[0]
            infostring.append(chr(resp))

        sleep(0.1)

        return ''.join(infostring)