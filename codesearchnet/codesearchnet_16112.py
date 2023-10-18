def sign(self, value):
        """
        :type value: any
        :rtype: bytes
        """
        payload = struct.pack('>cQ', self.version, int(time.time()))
        payload += force_bytes(value)
        return payload + self.signature(payload).finalize()