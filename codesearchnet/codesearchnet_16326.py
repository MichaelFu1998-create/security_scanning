def set_fan_power(self, power):
        """Set only the Fan power.

        :param power: Fan power value as an integer between 0-255.

        :type power: int

        :rtype: boolean

        :Example:

        >>> alpha.set_fan_power(255)
        True
        """
        # Check to make sure the value is a single byte
        if power > 255:
            raise ValueError("The fan power should be a single byte (0-255).")

        # Send the command byte and wait 10 ms
        a = self.cnxn.xfer([0x42])[0]
        sleep(10e-3)

        # Send the next two bytes
        b = self.cnxn.xfer([0x00])[0]
        c = self.cnxn.xfer([power])[0]

        sleep(0.1)

        return True if a == 0xF3 and b == 0x42 and c == 0x00 else False