def _derive_checksum(self, s):
        """ Derive the checksum

            :param str s: Random string for which to derive the checksum
        """
        checksum = hashlib.sha256(bytes(s, "ascii")).hexdigest()
        return checksum[:4]