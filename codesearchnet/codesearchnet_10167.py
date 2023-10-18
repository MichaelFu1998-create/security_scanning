def vcl(self, name, content):
        """ Create a new VCL under this version. """
        vcl = VCL()
        vcl.conn = self.conn

        vcl.attrs = {
            # Parent params
            'service_id': self.attrs['service_id'],
            'version': self.attrs['number'],

            # New instance params
            'name': name,
            'content': content,
        }

        vcl.save()

        return vcl