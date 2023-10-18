def register(self, cls):
        """
        Adds a preview to the index.
        """
        preview = cls(site=self)
        logger.debug('Registering %r with %r', preview, self)
        index = self.__previews.setdefault(preview.module, {})
        index[cls.__name__] = preview