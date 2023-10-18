def create(self, **kwargs):
        """
            Create the tag.
        """
        for attr in kwargs.keys():
            setattr(self, attr, kwargs[attr])

        params = {"name": self.name}

        output = self.get_data("tags", type="POST", params=params)
        if output:
            self.name = output['tag']['name']
            self.resources = output['tag']['resources']