def load(self, clear=False):
        """
        Loads all the config plugin modules to build a working configuration.

        If there is a ``localconfig`` module on the python path, it will be
        loaded last, overriding other settings.

        :param bool clear: Clear out the previous settings before loading

        """
        if clear:
            self.settings = {}

        defer = []

        # Load all config plugins
        for conf in pkg_resources.iter_entry_points('pyconfig'):
            if conf.attrs:
                raise RuntimeError("config must be a module")

            mod_name = conf.module_name
            base_name = conf.name if conf.name != 'any' else None

            log.info("Loading module '%s'", mod_name)
            mod_dict = runpy.run_module(mod_name)

            # If this module wants to be deferred, save it for later
            if mod_dict.get('deferred', None) is deferred:
                log.info("Deferring module '%s'", mod_name)
                mod_dict.pop('deferred')
                defer.append((mod_name, base_name, mod_dict))
                continue

            self._update(mod_dict, base_name)

        # Load deferred modules
        for mod_name, base_name, mod_dict in defer:
            log.info("Loading deferred module '%s'", mod_name)
            self._update(mod_dict, base_name)

        if etcd().configured:
            # Load etcd stuff
            mod_dict = etcd().load()
            if mod_dict:
                self._update(mod_dict)

        # Allow localconfig overrides
        mod_dict = None
        try:
            mod_dict = runpy.run_module('localconfig')
        except ImportError:
            pass
        except ValueError as err:
            if getattr(err, 'message') != '__package__ set to non-string':
                raise

            # This is a bad work-around to make this work transparently...
            # shouldn't really access core stuff like this, but Fuck It[tm]
            mod_name = 'localconfig'
            if sys.version_info < (2, 7):
                loader, code, fname = runpy._get_module_details(mod_name)
            else:
                _, loader, code, fname = runpy._get_module_details(mod_name)
            mod_dict = runpy._run_code(code, {}, {}, mod_name, fname, loader,
                    pkg_name=None)

        if mod_dict:
            log.info("Loading module 'localconfig'")
            self._update(mod_dict)

        self.call_reload_hooks()