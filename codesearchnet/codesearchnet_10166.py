def version(self):
        """ Create a new version under this service. """
        ver = Version()
        ver.conn = self.conn

        ver.attrs = {
            # Parent params
            'service_id': self.attrs['id'],
        }

        ver.save()

        return ver