def off(self):
        """Turn OFF the OPC (fan and laser)

        :returns: boolean success state
        """
        b1 = self.cnxn.xfer([0x03])[0]          # send the command byte
        sleep(9e-3)                             # sleep for 9 ms

        return True if b1 == 0xF3 else False