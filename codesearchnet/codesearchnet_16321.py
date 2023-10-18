def off(self):
        """Turn OFF the OPC (fan and laser)

        :rtype: boolean

        :Example:

        >>> alpha.off()
        True
        """
        b1 = self.cnxn.xfer([0x03])[0]          # send the command byte
        sleep(9e-3)                             # sleep for 9 ms
        b2 = self.cnxn.xfer([0x01])[0]          # send the following two bytes
        sleep(0.1)

        return True if b1 == 0xF3 and b2 == 0x03 else False