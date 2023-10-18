def get_object(cls, api_token, domain_name):
        """
            Class method that will return a Domain object by ID.
        """
        domain = cls(token=api_token, name=domain_name)
        domain.load()
        return domain