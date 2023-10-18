def ip_address(self):
        """
        Public ip_address
        """
        ip = None
        for eth in self.networks['v4']:
            if eth['type'] == 'public':
                ip = eth['ip_address']
                break
        if ip is None:
            raise ValueError("No public IP found")
        return ip