def record_by_name(self, hostname):
        """
        Returns dictionary with city data containing `country_code`, `country_name`,
        `region`, `city`, `postal_code`, `latitude`, `longitude`, `dma_code`,
        `metro_code`, `area_code`, `region_code` and `time_zone`.

        :arg hostname: Hostname (e.g. example.com)
        """
        addr = self._gethostbyname(hostname)
        return self.record_by_addr(addr)