def get_xdg_home(self):
        # type: () -> str
        """
        Returns the value specified in the XDG_CONFIG_HOME environment variable
        or the appropriate default.
        """
        config_home = getenv('XDG_CONFIG_HOME', '')
        if config_home:
            self._log.debug('XDG_CONFIG_HOME is set to %r', config_home)
            return expanduser(join(config_home, self.group_name, self.app_name))
        return expanduser('~/.config/%s/%s' % (self.group_name, self.app_name))