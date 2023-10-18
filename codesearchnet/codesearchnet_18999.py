def _string_data(self, data):
        """
        This method handles the incoming string data message from Firmata.
        The string is printed to the console

        :param data: Message data from Firmata

        :return: No return value.s
        """
        print("_string_data:")
        string_to_print = []
        for i in data[::2]:
            string_to_print.append(chr(i))
        print("".join(string_to_print))