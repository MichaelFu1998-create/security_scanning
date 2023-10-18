def uninstall_blacklisted(self):
        """
        Uninstalls all blacklisted packages.
        """
        from burlap.system import distrib_family
        blacklisted_packages = self.env.blacklisted_packages
        if not blacklisted_packages:
            print('No blacklisted packages.')
            return
        else:
            family = distrib_family()
            if family == DEBIAN:
                self.sudo('DEBIAN_FRONTEND=noninteractive apt-get -yq purge %s' % ' '.join(blacklisted_packages))
            else:
                raise NotImplementedError('Unknown family: %s' % family)