def i2c_reply(self, data):
        """
        This method receives replies to i2c_read requests. It stores the data for each i2c device
        address in a dictionary called i2c_map. The data is retrieved via a call to i2c_get_read_data()
        in pymata.py
        It a callback was specified in pymata.i2c_read, the raw data is sent through the callback

        :param data: raw data returned from i2c device
        """

        reply_data = []
        address = (data[0] & 0x7f) + (data[1] << 7)
        register = data[2] & 0x7f + data[3] << 7
        reply_data.append(register)
        for i in range(4, len(data), 2):
            data_item = (data[i] & 0x7f) + (data[i + 1] << 7)
            reply_data.append(data_item)
        # retrieve the data entry for this address from the i2c map
        if address in self.i2c_map:
            i2c_data = self.i2c_map.get(address, None)

            i2c_data[1] = reply_data
            self.i2c_map[address] = i2c_data
            # is there a call back for this entry?
            # if yes, return a list of bytes through the callback
            if i2c_data[0] is not None:
                i2c_data[0]([self.pymata.I2C, address, reply_data])