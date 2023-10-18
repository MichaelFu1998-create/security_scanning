def HMAC(self, key, str_):
        """The HMAC(key, str) function."""
        # pylint: disable=C0103
        return hmac.new(key, str_, self.hash_factory).digest()