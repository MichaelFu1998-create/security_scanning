def i2c_get_read_data(self, address):
        """
        This method retrieves the i2c read data as the result of an i2c_read() command.

        :param address: i2c device address

        :return: raw data read from device
        """
        if address in self._command_handler.i2c_map:
            map_entry = self._command_handler.i2c_map[address]
            return map_entry[1]