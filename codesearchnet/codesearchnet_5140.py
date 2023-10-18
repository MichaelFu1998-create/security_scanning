def get_records(self, params=None):
        """
            Returns a list of Record objects
        """
        if params is None:
            params = {}
        
        # URL https://api.digitalocean.com/v2/domains/[NAME]/records/
        records = []
        data = self.get_data("domains/%s/records/" % self.name, type=GET, params=params)

        for record_data in data['domain_records']:

            record = Record(domain_name=self.name, **record_data)
            record.token = self.token
            records.append(record)

        return records