def get_version(self): 
        """
        Get distribution version.

        This method is enhanced compared to original distutils implementation.
        If the version string is set to a special value then instead of using
        the actual value the real version is obtained by querying versiontools.

        If versiontools package is not installed then the version is obtained
        from the standard section of the ``PKG-INFO`` file. This file is
        automatically created by any source distribution. This method is less
        useful as it cannot take advantage of version control information that
        is automatically loaded by versiontools. It has the advantage of not
        requiring versiontools installation and that it does not depend on
        ``setup_requires`` feature of ``setuptools``.
        """
        if (self.name is not None and self.version is not None
            and self.version.startswith(":versiontools:")):
            return (self.__get_live_version() or self.__get_frozen_version()
                    or self.__fail_to_get_any_version())
        else:
            return self.__base.get_version(self)