def create(self, name, ip_address):
        """
        Creates a new domain

        Parameters
        ----------
        name: str
            new domain name
        ip_address: str
            IP address for the new domain
        """
        return (self.post(name=name, ip_address=ip_address)
                .get(self.singular, None))