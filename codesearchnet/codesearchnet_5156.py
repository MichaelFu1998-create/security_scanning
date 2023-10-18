def get_all_droplets(self, tag_name=None):
        """
            This function returns a list of Droplet object.
        """
        params = dict()
        if tag_name:
            params["tag_name"] = tag_name

        data = self.get_data("droplets/", params=params)

        droplets = list()
        for jsoned in data['droplets']:
            droplet = Droplet(**jsoned)
            droplet.token = self.token

            for net in droplet.networks['v4']:
                if net['type'] == 'private':
                    droplet.private_ip_address = net['ip_address']
                if net['type'] == 'public':
                    droplet.ip_address = net['ip_address']
            if droplet.networks['v6']:
                droplet.ip_v6_address = droplet.networks['v6'][0]['ip_address']

            if "backups" in droplet.features:
                droplet.backups = True
            else:
                droplet.backups = False
            if "ipv6" in droplet.features:
                droplet.ipv6 = True
            else:
                droplet.ipv6 = False
            if "private_networking" in droplet.features:
                droplet.private_networking = True
            else:
                droplet.private_networking = False

            droplets.append(droplet)

        return droplets