def on(self):
        """Turn ON the OPC (fan and laser)

        :rtype: boolean

        :Example:

        >>> alpha.on()
        True
        """
        b1 = self.cnxn.xfer([0x03])[0]          # send the command byte
        sleep(9e-3)                             # sleep for 9 ms
        b2, b3 = self.cnxn.xfer([0x00, 0x01])   # send the following byte
        sleep(0.1)

        return True if b1 == 0xF3 and b2 == 0x03 else False