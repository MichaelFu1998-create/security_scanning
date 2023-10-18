def load(self, reload=False, require_load=False):
        # type: (bool, bool) -> None
        """
        Searches for an appropriate config file. If found, loads the file into
        the current instance. This method can also be used to reload a
        configuration. Note that you may want to set ``reload`` to ``True`` to
        clear the configuration before loading in that case.  Without doing
        that, values will remain available even if they have been removed from
        the config files.

        :param reload: if set to ``True``, the existing values are cleared
                       before reloading.
        :param require_load: If set to ``True`` this will raise a
                             :py:exc:`IOError` if no config file has been found
                             to load.
        """

        if reload:  # pragma: no cover
            self.config = None

        # only load the config if necessary (or explicitly requested)
        if self.config:  # pragma: no cover
            self._log.debug('Returning cached config instance. Use '
                            '``reload=True`` to avoid caching!')
            return

        path = self._effective_path()
        config_filename = self._effective_filename()

        # Next, use the resolved path to find the filenames. Keep track of
        # which files we loaded in order to inform the user.
        self._active_path = [join(_, config_filename) for _ in path]
        for dirname in path:
            conf_name = join(dirname, config_filename)
            readable = self.check_file(conf_name)
            if readable:
                action = 'Updating' if self._loaded_files else 'Loading initial'
                self._log.info('%s config from %s', action, conf_name)
                self.read(conf_name)
                if conf_name == expanduser("~/.%s/%s/%s" % (
                        self.group_name, self.app_name, self.filename)):
                    self._log.warning(
                        "DEPRECATION WARNING: The file "
                        "'%s/.%s/%s/app.ini' was loaded. The XDG "
                        "Basedir standard requires this file to be in "
                        "'%s/.config/%s/%s/app.ini'! This location "
                        "will no longer be parsed in a future version of "
                        "config_resolver! You can already (and should) move "
                        "the file!", expanduser("~"), self.group_name,
                        self.app_name, expanduser("~"), self.group_name,
                        self.app_name)
                self._loaded_files.append(conf_name)

        if not self._loaded_files and not require_load:
            self._log.warning(
                "No config file named %s found! Search path was %r",
                config_filename,
                path)
        elif not self._loaded_files and require_load:
            raise IOError("No config file named %s found! Search path "
                          "was %r" % (config_filename, path))