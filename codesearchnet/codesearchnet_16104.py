def encrypt(self, data):
        """
        :type data: any
        :rtype: any
        """
        data = force_bytes(data)
        iv = os.urandom(16)
        return self._encrypt_from_parts(data, iv)