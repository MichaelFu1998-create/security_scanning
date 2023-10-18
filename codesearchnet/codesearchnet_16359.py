def monitorTUN(self):
        """
        Monitors the TUN adapter and sends data over serial port.

        Returns:
            ret: Number of bytes sent over serial port
        """
        packet = self.checkTUN()

        if packet:
            try:
                # TODO Do I need to strip off [4:] before sending?
                ret = self._faraday.send(packet)
                return ret

            except AttributeError as error:
                # AttributeError was encounteredthreading.Event()
                print("AttributeError")