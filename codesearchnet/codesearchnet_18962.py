def i2c_stop_reading(self, address):
        """
        This method stops an I2C_READ_CONTINUOUSLY operation for the i2c device address specified.

        :param address: address of i2c device
        """
        data = [address, self.I2C_STOP_READING]
        self._command_handler.send_sysex(self._command_handler.I2C_REQUEST, data)