def enable_mods(self):
        """
        Enables all modules in the current module list.
        Does not disable any currently enabled modules not in the list.
        """
        r = self.local_renderer
        for mod_name in r.env.mods_enabled:
            with self.settings(warn_only=True):
                self.enable_mod(mod_name)