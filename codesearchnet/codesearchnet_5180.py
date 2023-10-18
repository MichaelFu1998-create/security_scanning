def get_firewall(self, firewall_id):
        """
            Return a Firewall by its ID.
        """
        return Firewall.get_object(
            api_token=self.token,
            firewall_id=firewall_id,
        )