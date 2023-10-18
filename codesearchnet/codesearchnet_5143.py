def load(self):
        """
            Load the FloatingIP object from DigitalOcean.

            Requires self.ip to be set.
        """
        data = self.get_data('floating_ips/%s' % self.ip, type=GET)
        floating_ip = data['floating_ip']

        # Setting the attribute values
        for attr in floating_ip.keys():
            setattr(self, attr, floating_ip[attr])

        return self