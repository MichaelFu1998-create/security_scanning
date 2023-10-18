def receive(self, length):
        """Reads in data from a serial port (length bytes), decodes SLIP packets

        A function which reads from the serial port and then uses the SlipLib
        module to decode the SLIP protocol packets. Each message received
        is added to a receive buffer in SlipLib which is then returned.

        Args:
            length (int): Length to receive with serialPort.read(length)

        Returns:
            bytes: An iterator of the receive buffer

        """

        # Create a sliplib Driver
        slipDriver = sliplib.Driver()

        # Receive data from serial port
        ret = self._serialPort.read(length)

        # Decode data from slip format, stores msgs in sliplib.Driver.messages
        temp = slipDriver.receive(ret)
        return iter(temp)