def ping(self):
        """Checks the connection between the Raspberry Pi and the OPC

        :rtype: Boolean
        """
        b = self.cnxn.xfer([0xCF])[0]           # send the command byte

        sleep(0.1)

        return True if b == 0xF3 else False