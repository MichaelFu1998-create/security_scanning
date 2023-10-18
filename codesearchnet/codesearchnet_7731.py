def time_zone_by_name(self, hostname):
        """
        Returns time zone in tzdata format (e.g. America/New_York or Europe/Paris)

        :arg hostname: Hostname (e.g. example.com)
        """
        addr = self._gethostbyname(hostname)
        return self.time_zone_by_addr(addr)