def records(self, name):
        """
        Get a list of all domain records for the given domain name

        Parameters
        ----------
        name: str
            domain name
        """
        if self.get(name):
            return DomainRecords(self.api, name)