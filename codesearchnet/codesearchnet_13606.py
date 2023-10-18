def _compute_handshake(self):
        """Compute the authentication handshake value.

        :return: the computed hash value.
        :returntype: `str`"""
        return hashlib.sha1(to_utf8(self.stream_id)+to_utf8(self.secret)).hexdigest()