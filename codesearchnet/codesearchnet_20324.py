def by_name(self, name):
        """
        Retrieve a droplet by name (return first if duplicated)

        Parameters
        ----------
        name: str
            droplet name

        Returns
        -------
        droplet: DropletActions
        """
        for d in self.list():
            if d['name'] == name:
                return self.get(d['id'])
        raise KeyError("Could not find droplet with name %s" % name)