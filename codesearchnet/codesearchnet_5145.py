def reserve(self, *args, **kwargs):
        """
            Creates a FloatingIP in a region without assigning
            it to a specific Droplet.

            Note: Every argument and parameter given to this method will be
            assigned to the object.

            Args:
                region_slug: str - region's slug (e.g. 'nyc3')
        """
        data = self.get_data('floating_ips/',
                             type=POST,
                             params={'region': self.region_slug})

        if data:
            self.ip = data['floating_ip']['ip']
            self.region = data['floating_ip']['region']

        return self