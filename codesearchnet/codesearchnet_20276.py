def load_plugin(self, name):
        """This automatically loads a plugin by the given name from the
        current source and returns the module.  This is a convenient
        alternative to the import statement and saves you from invoking
        ``__import__`` or a similar function yourself.

        :param name: the name of the plugin to load.
        """
        if '.' in name:
            raise ImportError('Plugin names cannot contain dots.')
        with self:
            return __import__(self.base.package + '.' + name,
                              globals(), {}, ['__name__'])