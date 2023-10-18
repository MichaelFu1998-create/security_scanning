def unsign(self, signed_value, ttl=None):
        """
        Retrieve original value and check it wasn't signed more
        than max_age seconds ago.

        :type signed_value: bytes
        :type ttl: int | datetime.timedelta
        """
        h_size, d_size = struct.calcsize('>cQ'), self.digest.digest_size
        fmt = '>cQ%ds%ds' % (len(signed_value) - h_size - d_size, d_size)
        try:
            version, timestamp, value, sig = struct.unpack(fmt, signed_value)
        except struct.error:
            raise BadSignature('Signature is not valid')
        if version != self.version:
            raise BadSignature('Signature version not supported')
        if ttl is not None:
            if isinstance(ttl, datetime.timedelta):
                ttl = ttl.total_seconds()
            # Check timestamp is not older than ttl
            age = abs(time.time() - timestamp)
            if age > ttl + _MAX_CLOCK_SKEW:
                raise SignatureExpired('Signature age %s > %s seconds' % (age,
                                                                          ttl))
        try:
            self.signature(signed_value[:-d_size]).verify(sig)
        except InvalidSignature:
            raise BadSignature(
                'Signature "%s" does not match' % binascii.b2a_base64(sig))
        return value