def country_name_by_name(self, hostname):
        """
        Returns full country name for specified hostname.

        :arg hostname: Hostname (e.g. example.com)
        """
        addr = self._gethostbyname(hostname)
        return self.country_name_by_addr(addr)