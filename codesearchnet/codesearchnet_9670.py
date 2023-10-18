def _get_digest(self):
        """Return message digest if a secret key was provided"""

        return hmac.new(
            self._secret, request.data, hashlib.sha1).hexdigest() if self._secret else None