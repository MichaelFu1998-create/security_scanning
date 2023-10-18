def load(self):
        """
            Load the Certificate object from DigitalOcean.

            Requires self.id to be set.
        """
        data = self.get_data("certificates/%s" % self.id)
        certificate = data["certificate"]

        for attr in certificate.keys():
            setattr(self, attr, certificate[attr])

        return self