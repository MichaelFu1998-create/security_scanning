def private_ip(self):
        """
        Private ip_address
        """
        ip = None
        for eth in self.networks['v4']:
            if eth['type'] == 'private':
                ip = eth['ip_address']
                break
        if ip is None:
            raise ValueError("No private IP found")
        return ip