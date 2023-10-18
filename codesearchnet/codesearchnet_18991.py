def report_firmware(self, data):
        """
        This method processes the report firmware message,  sent asynchronously by Firmata when it starts up
        or after refresh_report_firmware() is called
        
        Use the api method api_get_firmware_version to retrieve this information

        :param data: Message data from Firmata

        :return: No return value.
        """
        self.firmata_firmware.append(data[0])  # add major
        self.firmata_firmware.append(data[1])  # add minor

        # extract the file name string from the message
        # file name is in bytes 2 to the end
        name_data = data[2:]

        # constructed file name
        file_name = []

        # the file name is passed in with each character as 2 bytes, the high order byte is equal to 0
        # so skip over these zero bytes
        for i in name_data[::2]:
            file_name.append(chr(i))

        # add filename to tuple
        self.firmata_firmware.append("".join(file_name))