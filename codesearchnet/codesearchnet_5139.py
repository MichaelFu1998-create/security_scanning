def create(self):
        """
            Create new doamin
        """
        # URL https://api.digitalocean.com/v2/domains
        data = {
            "name": self.name,
            "ip_address": self.ip_address,
        }

        domain = self.get_data("domains", type=POST, params=data)
        return domain