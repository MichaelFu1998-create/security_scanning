def refresh(self, *args, **kwargs):
        """
        Updates/upgrades all system packages.
        """
        r = self.local_renderer
        packager = self.packager
        if packager == APT:
            r.sudo('DEBIAN_FRONTEND=noninteractive apt-get -yq update --fix-missing')
        elif packager == YUM:
            raise NotImplementedError
            #return upgrade_yum(*args, **kwargs)
        else:
            raise Exception('Unknown packager: %s' % (packager,))