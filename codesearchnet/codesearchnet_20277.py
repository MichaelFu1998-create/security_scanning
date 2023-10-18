def open_resource(self, plugin, filename):
        """This function locates a resource inside the plugin and returns
        a byte stream to the contents of it.  If the resource cannot be
        loaded an :exc:`IOError` will be raised.  Only plugins that are
        real Python packages can contain resources.  Plain old Python
        modules do not allow this for obvious reasons.

        .. versionadded:: 0.3

        :param plugin: the name of the plugin to open the resource of.
        :param filename: the name of the file within the plugin to open.
        """
        mod = self.load_plugin(plugin)
        fn = getattr(mod, '__file__', None)
        if fn is not None:
            if fn.endswith(('.pyc', '.pyo')):
                fn = fn[:-1]
            if os.path.isfile(fn):
                return open(os.path.join(os.path.dirname(fn), filename), 'rb')
        buf = pkgutil.get_data(self.mod.__name__ + '.' + plugin, filename)
        if buf is None:
            raise IOError(errno.ENOEXITS, 'Could not find resource')
        return NativeBytesIO(buf)