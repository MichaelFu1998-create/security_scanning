def _set_perms(self, perms):
        """
        Sets the access permissions of the map.

        :param perms: the new permissions.
        """
        assert isinstance(perms, str) and len(perms) <= 3 and perms.strip() in ['', 'r', 'w', 'x', 'rw', 'r x', 'rx', 'rwx', 'wx', ]
        self._perms = perms