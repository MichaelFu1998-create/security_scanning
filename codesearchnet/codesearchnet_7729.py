def region_by_name(self, hostname):
        """
        Returns dictionary containing `country_code` and `region_code`.

        :arg hostname: Hostname (e.g. example.com)
        """
        addr = self._gethostbyname(hostname)
        return self.region_by_addr(addr)