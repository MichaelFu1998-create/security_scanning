def country_code_by_name(self, hostname):
        """
        Returns 2-letter country code (e.g. US) from hostname.

        :arg hostname: Hostname (e.g. example.com)
        """
        addr = self._gethostbyname(hostname)
        return self.country_code_by_addr(addr)