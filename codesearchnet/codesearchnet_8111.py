def get_device_id(self, dev):
        """Get device ID at given address/path.

        :param str dev: Serial device address/path
        :param baudrate: Baudrate to use when connecting (optional)
        """
        com, code, ok = io.send_packet(CMDTYPE.GETID, 0, dev, self.baudrate, 5)
        if code is None:
            self.error(action='get_device_id')
        return code