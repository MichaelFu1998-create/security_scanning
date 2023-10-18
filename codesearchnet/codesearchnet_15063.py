def decryptMessage(self, ciphertext, header, ad = None):
        """
        Decrypt a message using this double ratchet session.

        :param ciphertext: A bytes-like object encoding the message to decrypt.
        :param header: An instance of the Header class. This should have been sent
            together with the ciphertext.
        :param ad: A bytes-like object encoding the associated data to use for message
            authentication. Pass None to use the associated data set during construction.
        :returns: The plaintext.

        :raises AuthenticationFailedException: If checking the authentication for this
            message failed.
        :raises NotInitializedException: If this double ratchet session is not yet
            initialized with a key pair, thus not prepared to decrypt an incoming message.
        :raises TooManySavedMessageKeysException: If more than message_key_store_max have
            to be stored to decrypt this message.
        """

        if ad == None:
            ad = self.__ad

        # Try to decrypt the message using a previously saved message key
        plaintext = self.__decryptSavedMessage(ciphertext, header, ad)
        if plaintext:
            return plaintext

        # Check, whether the public key will trigger a dh ratchet step
        if self.triggersStep(header.dh_pub):
            # Save missed message keys for the current receiving chain
            self.__saveMessageKeys(header.pn)

            # Perform the step
            self.step(header.dh_pub)

        # Save missed message keys for the current receiving chain
        self.__saveMessageKeys(header.n)

        # Finally decrypt the message and return the plaintext
        return self.__decrypt(
            ciphertext,
            self.__skr.nextDecryptionKey(),
            header,
            ad
        )