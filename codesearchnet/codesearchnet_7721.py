def netspeed_by_name(self, hostname):
        """
        Returns NetSpeed name from hostname. Can be Unknown, Dial-up,
        Cable, or Corporate.

        :arg hostname: Hostname (e.g. example.com)
        """
        addr = self._gethostbyname(hostname)
        return self.netspeed_by_addr(addr)