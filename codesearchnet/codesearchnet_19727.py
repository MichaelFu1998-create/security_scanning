def set_netmask(self, netmask):
        """Change the current netmask."""
        self.set(ip=self._ip, netmask=netmask)