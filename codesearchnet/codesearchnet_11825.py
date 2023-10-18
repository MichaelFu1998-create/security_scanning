def update(self):
        """
        Preparse the packaging system for installations.
        """
        packager = self.packager
        if packager == APT:
            self.sudo('DEBIAN_FRONTEND=noninteractive apt-get -yq update')
        elif packager == YUM:
            self.sudo('yum update')
        else:
            raise Exception('Unknown packager: %s' % (packager,))