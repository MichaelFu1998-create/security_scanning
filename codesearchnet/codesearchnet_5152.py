def load_by_pub_key(self, public_key):
        """
            This method will load a SSHKey object from DigitalOcean
            from a public_key. This method will avoid problems like
            uploading the same public_key twice.
        """

        data = self.get_data("account/keys/")
        for jsoned in data['ssh_keys']:
            if jsoned.get('public_key', "") == public_key:
                self.id = jsoned['id']
                self.load()
                return self
        return None