def install_custom(self, *args, **kwargs):
        """
        Installs all system packages listed in the appropriate
        <packager>-requirements.txt.
        """
        if not self.env.manage_custom:
            return
        packager = self.packager
        if packager == APT:
            return self.install_apt(*args, **kwargs)
        elif packager == YUM:
            return self.install_yum(*args, **kwargs)
        else:
            raise NotImplementedError('Unknown packager: %s' % (packager,))