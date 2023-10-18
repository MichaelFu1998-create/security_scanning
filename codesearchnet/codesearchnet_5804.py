def sign(self, message):
        """Signs a message.

        Args:
            message: string, Message to be signed.

        Returns:
            string, The signature of the message for the given key.
        """
        message = _helpers._to_bytes(message, encoding='utf-8')
        return PKCS1_v1_5.new(self._key).sign(SHA256.new(message))