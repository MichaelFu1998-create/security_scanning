def encode(self) -> str:
        """
        Create a token based on the data held in the class.

        :return: A new token
        :rtype: str
        """
        payload = {}
        payload.update(self.registered_claims)
        payload.update(self.payload)
        return encode(self.secret, payload, self.alg, self.header)