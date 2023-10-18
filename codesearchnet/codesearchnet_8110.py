def set_device_id(self, dev, id):
        """Set device ID to new value.

        :param str dev: Serial device address/path
        :param id: Device ID to set
        """
        if id < 0 or id > 255:
            raise ValueError("ID must be an unsigned byte!")
        com, code, ok = io.send_packet(
            CMDTYPE.SETID, 1, dev, self.baudrate, 5, id)
        if not ok:
            raise_error(code)