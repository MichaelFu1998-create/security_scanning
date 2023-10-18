def register(self, what, obj):
        """
        Registering a plugin

        Params
        ------
        what: Nature of the plugin (backend, instrumentation, repo)
        obj: Instance of the plugin
        """
        # print("Registering pattern", name, pattern)
        name = obj.name
        version = obj.version
        enable = obj.enable
        if enable == 'n':
            return

        key = Key(name, version)
        self.plugins[what][key] = obj