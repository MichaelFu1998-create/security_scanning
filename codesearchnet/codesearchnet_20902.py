def get_xdg_dirs(self):
        # type: () -> List[str]
        """
        Returns a list of paths specified by the XDG_CONFIG_DIRS environment
        variable or the appropriate default.

        The list is sorted by precedence, with the most important item coming
        *last* (required by the existing config_resolver logic).
        """
        config_dirs = getenv('XDG_CONFIG_DIRS', '')
        if config_dirs:
            self._log.debug('XDG_CONFIG_DIRS is set to %r', config_dirs)
            output = []
            for path in reversed(config_dirs.split(':')):
                output.append(join(path, self.group_name, self.app_name))
            return output
        return ['/etc/xdg/%s/%s' % (self.group_name, self.app_name)]