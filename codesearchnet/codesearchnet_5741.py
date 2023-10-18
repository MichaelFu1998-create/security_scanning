def sign(self, message):
        """Signs a message.

        Args:
            message: bytes, Message to be signed.

        Returns:
            string, The signature of the message for the given key.
        """
        message = _helpers._to_bytes(message, encoding='utf-8')
        return rsa.pkcs1.sign(message, self._key, 'SHA-256')