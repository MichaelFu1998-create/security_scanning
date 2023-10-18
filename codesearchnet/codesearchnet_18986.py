def report_version(self, data):
        """
        This method processes the report version message,  sent asynchronously by Firmata when it starts up
        or after refresh_report_version() is called

        Use the api method api_get_version to retrieve this information
        
        :param data: Message data from Firmata
        
        :return: No return value.
        """
        self.firmata_version.append(data[0])  # add major
        self.firmata_version.append(data[1])