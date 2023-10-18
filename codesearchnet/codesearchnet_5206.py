def create(self):
        """
            Create the Certificate
        """
        params = {
            "name": self.name,
            "type": self.type,
            "dns_names": self.dns_names,
            "private_key": self.private_key,
            "leaf_certificate": self.leaf_certificate,
            "certificate_chain": self.certificate_chain
        }

        data = self.get_data("certificates/", type=POST, params=params)

        if data:
            self.id = data['certificate']['id']
            self.not_after = data['certificate']['not_after']
            self.sha1_fingerprint = data['certificate']['sha1_fingerprint']
            self.created_at = data['certificate']['created_at']
            self.type = data['certificate']['type']
            self.dns_names = data['certificate']['dns_names']
            self.state = data['certificate']['state']

        return self