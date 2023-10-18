def create(self, name, region, size, image, ssh_keys=None,
               backups=None, ipv6=None, private_networking=None, wait=True):
        """
        Create a new droplet

        Parameters
        ----------
        name: str
            Name of new droplet
        region: str
            slug for region (e.g., sfo1, nyc1)
        size: str
            slug for droplet size (e.g., 512mb, 1024mb)
        image: int or str
            image id (e.g., 12352) or slug (e.g., 'ubuntu-14-04-x64')
        ssh_keys: list, optional
            default SSH keys to be added on creation
            this is highly recommended for ssh access
        backups: bool, optional
            whether automated backups should be enabled for the Droplet.
            Automated backups can only be enabled when the Droplet is created.
        ipv6: bool, optional
            whether IPv6 is enabled on the Droplet
        private_networking: bool, optional
            whether private networking is enabled for the Droplet. Private
            networking is currently only available in certain regions
        wait: bool, default True
            if True then block until creation is complete
        """
        if ssh_keys and not isinstance(ssh_keys, (list, tuple)):
            raise TypeError("ssh_keys must be a list")
        resp = self.post(name=name, region=region, size=size, image=image,
                         ssh_keys=ssh_keys,
                         private_networking=private_networking,
                         backups=backups, ipv6=ipv6)
        droplet = self.get(resp[self.singular]['id'])
        if wait:
            droplet.wait()
        # HACK sometimes the IP address doesn't return correctly
        droplet = self.get(resp[self.singular]['id'])
        return droplet