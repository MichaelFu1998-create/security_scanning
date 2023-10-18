def register_plugin(self, plugin):
        """Registers a plugin and commands with the dispatcher for push()"""
        self.log.info("Registering plugin %s", type(plugin).__name__)
        self._register_commands(plugin)
        plugin.on_load()