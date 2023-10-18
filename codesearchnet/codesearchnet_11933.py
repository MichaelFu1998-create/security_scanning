def get_public_ip(self):
        """
        Gets the public IP for a host.
        """
        r = self.local_renderer
        ret = r.run(r.env.get_public_ip_command) or ''
        ret = ret.strip()
        print('ip:', ret)
        return ret