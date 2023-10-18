def save(self):
        """
            Save existing record
        """
        data = {
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
        return self.get_data(
            "domains/%s/records/%s" % (self.domain, self.id),
            type=PUT,
            params=data
        )