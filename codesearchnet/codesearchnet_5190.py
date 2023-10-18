def get_object(cls, api_token, domain, record_id):
        """
            Class method that will return a Record object by ID and the domain.
        """
        record = cls(token=api_token, domain=domain, id=record_id)
        record.load()
        return record