def _load_namespace(self, namespace, filename=None):
        """
        Initialise bot namespace with info in shoebot.data

        :param filename: Will be set to __file__ in the namespace
        """
        from shoebot import data
        for name in dir(data):
            namespace[name] = getattr(data, name)

        for name in dir(self):
            if name[0] != '_':
                namespace[name] = getattr(self, name)

        namespace['_ctx'] = self  # Used in older nodebox scripts.
        namespace['__file__'] = filename