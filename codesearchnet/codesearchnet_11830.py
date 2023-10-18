def upgrade(self, full=0):
        """
        Updates/upgrades all system packages.
        """
        full = int(full)
        r = self.local_renderer
        packager = self.packager
        if packager == APT:
            r.sudo('DEBIAN_FRONTEND=noninteractive apt-get -yq upgrade')
            if full:
                r.sudo('DEBIAN_FRONTEND=noninteractive apt-get dist-upgrade -yq')
        elif packager == YUM:
            raise NotImplementedError
        else:
            raise Exception('Unknown packager: %s' % (packager,))