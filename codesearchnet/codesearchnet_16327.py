def toggle_laser(self, state):
        """Toggle the power state of the laser.

        :param state: Boolean state of the laser

        :type state: boolean

        :rtype: boolean

        :Example:

        >>> alpha.toggle_laser(True)
        True
        """

        # Send the command byte and wait 10 ms
        a = self.cnxn.xfer([0x03])[0]

        sleep(10e-3)

        # If state is true, turn the laser ON, else OFF
        if state:
            b = self.cnxn.xfer([0x02])[0]
        else:
            b = self.cnxn.xfer([0x03])[0]

        sleep(0.1)

        return True if a == 0xF3 and b == 0x03 else False