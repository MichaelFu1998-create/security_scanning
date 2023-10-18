def create_new_domain_record(self, *args, **kwargs):
        """
            Create new domain record.
            https://developers.digitalocean.com/#create-a-new-domain-record

            Args:
                type: The record type (A, MX, CNAME, etc).
                name: The host name, alias, or service being defined by the record
                data: Variable data depending on record type.

            Optional Args:
                priority: The priority of the host
                port: The port that the service is accessible on
                weight: The weight of records with the same priority
        """
        data = {
            "type": kwargs.get("type", None),
            "name": kwargs.get("name", None),
            "data": kwargs.get("data", None)
        }

        #  Optional Args
        if kwargs.get("priority", None):
            data['priority'] = kwargs.get("priority", None)

        if kwargs.get("port", None):
            data['port'] = kwargs.get("port", None)

        if kwargs.get("weight", None):
            data['weight'] = kwargs.get("weight", None)

        return self.get_data(
            "domains/%s/records" % self.name,
            type=POST,
            params=data
        )