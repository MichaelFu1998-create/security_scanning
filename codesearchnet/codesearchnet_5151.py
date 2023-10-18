def load(self):
        """
            Load the SSHKey object from DigitalOcean.

            Requires either self.id or self.fingerprint to be set.
        """
        identifier = None
        if self.id:
            identifier = self.id
        elif self.fingerprint is not None:
            identifier = self.fingerprint

        data = self.get_data("account/keys/%s" % identifier, type=GET)

        ssh_key = data['ssh_key']

        # Setting the attribute values
        for attr in ssh_key.keys():
            setattr(self, attr, ssh_key[attr])
        self.id = ssh_key['id']