def create(self, *args, **kwargs):
        """
            Creates a FloatingIP and assigns it to a Droplet.

            Note: Every argument and parameter given to this method will be
            assigned to the object.

            Args:
                droplet_id: int - droplet id
        """
        data = self.get_data('floating_ips/',
                             type=POST,
                             params={'droplet_id': self.droplet_id})

        if data:
            self.ip = data['floating_ip']['ip']
            self.region = data['floating_ip']['region']

        return self