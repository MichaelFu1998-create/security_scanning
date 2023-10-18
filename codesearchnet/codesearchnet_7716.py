def id_by_name(self, hostname):
        """
        Returns the database ID for specified hostname.
        The id might be useful as array index. 0 is unknown.

        :arg hostname: Hostname to get ID from.
        """
        addr = self._gethostbyname(hostname)
        return self.id_by_addr(addr)