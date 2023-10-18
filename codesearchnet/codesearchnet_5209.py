def create(self):
        """
        Creates a new custom DigitalOcean Image from the Linux virtual machine
        image located at the provided `url`.
        """
        params = {'name': self.name,
                  'region': self.region,
                  'url': self.url,
                  'distribution': self.distribution,
                  'description': self.description,
                  'tags': self.tags}

        data = self.get_data('images', type=POST, params=params)

        if data:
            for attr in data['image'].keys():
                setattr(self, attr, data['image'][attr])

        return self