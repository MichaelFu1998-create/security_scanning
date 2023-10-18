def encryptMessage(self, message, ad = None):
        """
        Encrypt a message using this double ratchet session.

        :param message: A bytes-like object encoding the message to encrypt.
        :param ad: A bytes-like object encoding the associated data to use for message
            authentication. Pass None to use the associated data set during construction.
        :returns: A dictionary containing the message header and ciphertext. The header is
            required to synchronize the double ratchet of the receiving party. Send it
            along with the ciphertext.

        The returned dictionary consists of two keys: "header", which includes an instance
        of the Header class and "ciphertext", which includes the encrypted message encoded
        as a bytes-like object.

        :raises NotInitializedException: If this double ratchet session is not yet
            initialized with the other parties public key, thus not ready to encrypt a
            message to that party.
        """

        if ad == None:
            ad = self.__ad

        # Prepare the header for this message
        header = Header(
            self.pub,
            self.__skr.sending_chain_length,
            self.__skr.previous_sending_chain_length
        )

        # Encrypt the message
        ciphertext = self.__aead.encrypt(
            message,
            self.__skr.nextEncryptionKey(),
            self._makeAD(header, ad)
        )

        return {
            "header"     : header,
            "ciphertext" : ciphertext
        }