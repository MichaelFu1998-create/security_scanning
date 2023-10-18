def save_config_variables(self):
        """Save the configuration variables in non-volatile memory. This method
        should be used in conjuction with *write_config_variables*.

        :rtype: boolean

        :Example:

        >>> alpha.save_config_variables()
        True
        """
        command = 0x43
        byte_list = [0x3F, 0x3C, 0x3F, 0x3C, 0x43]
        success = [0xF3, 0x43, 0x3F, 0x3C, 0x3F, 0x3C]
        resp = []

        # Send the command byte and then wait for 10 ms
        r = self.cnxn.xfer([command])[0]
        sleep(10e-3)

        # append the response of the command byte to the List
        resp.append(r)

        # Send the rest of the config bytes
        for each in byte_list:
            r = self.cnxn.xfer([each])[0]
            resp.append(r)

        sleep(0.1)

        return True if resp == success else False