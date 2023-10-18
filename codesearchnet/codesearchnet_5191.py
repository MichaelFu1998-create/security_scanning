def create(self):
        """
        Creates a new record for a domain.

        Args:
            type (str): The type of the DNS record (e.g. A, CNAME, TXT).
            name (str): The host name, alias, or service being defined by the
                record.
            data (int): Variable data depending on record type.
            priority (int): The priority for SRV and MX records.
            port (int): The port for SRV records.
            ttl (int): The time to live for the record, in seconds.
            weight (int): The weight for SRV records.
            flags (int): An unsigned integer between 0-255 used for CAA records.
            tags (string): The parameter tag for CAA records. Valid values are
                "issue", "wildissue", or "iodef"
        """
        input_params = {
            "type": self.type,
            "data": self.data,
            "name": self.name,
            "priority": self.priority,
            "port": self.port,
            "ttl": self.ttl,
            "weight": self.weight,
            "flags": self.flags,
            "tags": self.tags
        }

        data = self.get_data(
            "domains/%s/records" % (self.domain),
            type=POST,
            params=input_params,
        )

        if data:
            self.id = data['domain_record']['id']