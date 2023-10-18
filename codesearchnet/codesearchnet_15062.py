def step(self, key, chain):
        """
        Perform a rachted step, replacing one of the internally managed chains with a new
        one.

        :param key: A bytes-like object encoding the key to initialize the replacement
            chain with.
        :param chain: The chain to replace. This parameter must be one of the two strings
            "sending" and "receiving".
        """

        if chain == "sending":
            self.__previous_sending_chain_length = self.sending_chain_length

            self.__sending_chain = self.__SendingChain(key)

        if chain == "receiving":
            self.__receiving_chain = self.__ReceivingChain(key)