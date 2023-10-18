def invalidate_ip(self, ip):
        """
        Invalidate httpBL cache for IP address

        :param ip: ipv4 IP address
        """

        if self._use_cache:
            key = self._make_cache_key(ip)
            self._cache.delete(key, version=self._cache_version)