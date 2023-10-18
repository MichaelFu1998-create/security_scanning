def verify(self, message, signature):
        """Verifies a message against a signature.

        Args:
        message: string or bytes, The message to verify. If string, will be
                 encoded to bytes as utf-8.
        signature: string or bytes, The signature on the message. If string,
                   will be encoded to bytes as utf-8.

        Returns:
            True if message was signed by the private key associated with the
            public key that this object was constructed with.
        """
        message = _helpers._to_bytes(message, encoding='utf-8')
        signature = _helpers._to_bytes(signature, encoding='utf-8')
        try:
            crypto.verify(self._pubkey, signature, message, 'sha256')
            return True
        except crypto.Error:
            return False