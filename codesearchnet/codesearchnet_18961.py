def i2c_write(self, address, *args):
        """
        Write data to an i2c device.

        :param address: i2c device address

        :param args: A variable number of bytes to be sent to the device
        """
        data = [address, self.I2C_WRITE]
        for item in args:
            data.append(item & 0x7f)
            data.append((item >> 7) & 0x7f)
        self._command_handler.send_sysex(self._command_handler.I2C_REQUEST, data)