def org_by_name(self, hostname):
        """
        Returns Organization, ISP, or ASNum name for given hostname.

        :arg hostname: Hostname (e.g. example.com)
        """
        addr = self._gethostbyname(hostname)
        return self.org_by_addr(addr)