def install_packages(self):
        """
        Installs all required packages listed for this satchel.
        Normally called indirectly by running packager.configure().
        """
        os_version = self.os_version
        package_list = self.get_package_list()
        if package_list:
            package_list_str = ' '.join(package_list)
            if os_version.distro == UBUNTU:
                self.sudo('apt-get update --fix-missing; DEBIAN_FRONTEND=noninteractive apt-get install --yes %s' % package_list_str)
            elif os_version.distro == DEBIAN:
                self.sudo('apt-get update --fix-missing; DEBIAN_FRONTEND=noninteractive apt-get install --yes %s' % package_list_str)
            elif os_version.distro == FEDORA:
                self.sudo('yum install --assumeyes %s' % package_list_str)
            else:
                raise NotImplementedError('Unknown distro: %s' % os_version.distro)