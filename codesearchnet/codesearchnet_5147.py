def get_object(cls, api_token, firewall_id):
        """
            Class method that will return a Firewall object by ID.
        """
        firewall = cls(token=api_token, id=firewall_id)
        firewall.load()
        return firewall