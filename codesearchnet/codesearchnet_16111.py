def signature(self, value):
        """
        :type value: any
        :rtype: HMAC
        """
        h = HMAC(self.key, self.digest, backend=settings.CRYPTOGRAPHY_BACKEND)
        h.update(force_bytes(value))
        return h