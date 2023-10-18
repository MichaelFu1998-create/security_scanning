def start(self):
        """Perform the App's actions as configured."""
        if self.extra_args:
            sys.exit('{} takes no extra arguments'.format(self.name))
        else:

            if self._toggle_value:
                nbextensions.install_nbextension_python(
                    _pkg_name, overwrite=True, symlink=False,
                    user=self.user, sys_prefix=self.sys_prefix, prefix=None,
                    nbextensions_dir=None, logger=None)
            else:
                nbextensions.uninstall_nbextension_python(
                    _pkg_name, user=self.user, sys_prefix=self.sys_prefix,
                    prefix=None, nbextensions_dir=None, logger=None)

            self.toggle_nbextension_python(_pkg_name)
            self.toggle_server_extension_python(_pkg_name)