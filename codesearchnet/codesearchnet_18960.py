def i2c_read(self, address, register, number_of_bytes, read_type, cb=None):
        """
        This method requests the read of an i2c device. Results are retrieved by a call to
        i2c_get_read_data().
        If a callback method is provided, when data is received from the device it will be sent to the callback method

        :param address: i2c device address

        :param register: register number (can be set to zero)

        :param number_of_bytes: number of bytes expected to be returned

        :param read_type: I2C_READ  or I2C_READ_CONTINUOUSLY

        :param cb: Optional callback function to report i2c data as result of read command
        """
        data = [address, read_type, register & 0x7f, (register >> 7) & 0x7f,
                number_of_bytes & 0x7f, (number_of_bytes >> 7) & 0x7f]

        # add or update entry in i2c_map for reply
        self._command_handler.i2c_map[address] = [cb, None]

        self._command_handler.send_sysex(self._command_handler.I2C_REQUEST, data)