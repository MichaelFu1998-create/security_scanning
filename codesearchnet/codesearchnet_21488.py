def writerow(self, observation_data):
        """
        Writes a single observation to the output file.

        If the ``observation_data`` parameter is a dictionary, it is
        converted to a list to keep a consisted field order (as described
        in format specification). Otherwise it is assumed that the data
        is a raw record ready to be written to file.

        :param observation_data: a single observation as a dictionary or list
        """
        if isinstance(observation_data, (list, tuple)):
            row = observation_data
        else:
            row = self.dict_to_row(observation_data)
        self.writer.writerow(row)