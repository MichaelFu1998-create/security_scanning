def next(self, data):
        """
        Derive a new set of internal and output data from given input data and the data
        stored internally.

        Use the key derivation function to derive new data. The kdf gets supplied with the
        current key and the data passed to this method.

        :param data: A bytes-like object encoding the data to pass to the key derivation
            function.
        :returns: A bytes-like object encoding the output material.
        """

        self.__length += 1

        result = self.__kdf.calculate(self.__key, data, 64)
        self.__key = result[:32]
        return result[32:]