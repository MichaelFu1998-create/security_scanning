def list_plugins(self):
        """Returns a sorted list of all plugins that are available in this
        plugin source.  This can be useful to automatically discover plugins
        that are available and is usually used together with
        :meth:`load_plugin`.
        """
        rv = []
        for _, modname, ispkg in pkgutil.iter_modules(self.mod.__path__):
            rv.append(modname)
        return sorted(rv)