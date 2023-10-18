def cf_data_to_bytes(value):
        """
        Extracts a bytestring from a CFData object

        :param value:
            A CFData object

        :return:
            A byte string
        """

        start = CoreFoundation.CFDataGetBytePtr(value)
        num_bytes = CoreFoundation.CFDataGetLength(value)
        return string_at(start, num_bytes)