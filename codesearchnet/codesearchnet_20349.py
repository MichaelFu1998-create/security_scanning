def get(self, id, **kwargs):
        """
        Retrieve a single domain record given the id
        """
        return super(DomainRecords, self).get(id, **kwargs)