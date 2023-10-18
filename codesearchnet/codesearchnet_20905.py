def _effective_path(self):
        # type: () -> List[str]
        """
        Returns a list of paths to search for config files in reverse order of
        precedence.  In other words: the last path element will override the
        settings from the first one.
        """
        # default search path
        path = (['/etc/%s/%s' % (self.group_name, self.app_name)] +
                self.get_xdg_dirs() +
                [expanduser('~/.%s/%s' % (self.group_name, self.app_name)),
                 self.get_xdg_home(),
                 join(getcwd(), '.{}'.format(self.group_name), self.app_name)])

        # If a path was passed directly to this instance, override the path.
        if self.search_path:
            path = self.search_path.split(pathsep)

        # Next, consider the environment variables...
        env_path = getenv(self.env_path_name)

        if env_path and env_path.startswith('+'):
            # If prefixed with a '+', append the path elements
            additional_paths = env_path[1:].split(pathsep)
            self._log.info('Search path extended with %r by the environment '
                           'variable %s.',
                           additional_paths,
                           self.env_path_name)
            path.extend(additional_paths)
        elif env_path:
            # Otherwise, override again. This takes absolute precedence.
            self._log.info("Configuration search path was overridden with "
                           "%r by the environment variable %r.",
                           env_path,
                           self.env_path_name)
            path = env_path.split(pathsep)

        return path