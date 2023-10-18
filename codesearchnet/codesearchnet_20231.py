def discover_all_plugins(self):
        """
        Load all plugins from dgit extension
        """
        for v in pkg_resources.iter_entry_points('dgit.plugins'):
            m = v.load()
            m.setup(self)