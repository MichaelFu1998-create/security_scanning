def load(self):
        """
           Fetch data about droplet - use this instead of get_data()
        """
        droplets = self.get_data("droplets/%s" % self.id)
        droplet = droplets['droplet']

        for attr in droplet.keys():
            setattr(self, attr, droplet[attr])

        for net in self.networks['v4']:
            if net['type'] == 'private':
                self.private_ip_address = net['ip_address']
            if net['type'] == 'public':
                self.ip_address = net['ip_address']
        if self.networks['v6']:
            self.ip_v6_address = self.networks['v6'][0]['ip_address']

            if "backups" in self.features:
                self.backups = True
            else:
                self.backups = False
            if "ipv6" in self.features:
                self.ipv6 = True
            else:
                self.ipv6 = False
            if "private_networking" in self.features:
                self.private_networking = True
            else:
                self.private_networking = False

        if "tags" in droplets:
            self.tags = droplets["tags"]

        return self