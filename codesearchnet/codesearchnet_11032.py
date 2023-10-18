def get_loader(self, meta: ResourceDescription, raise_on_error=False) -> BaseLoader:
        """
        Attempts to get a loader

        :param meta: The resource description instance
        :param raise_on_error: Raise ImproperlyConfigured if the loader cannot be resolved
        :returns: The requested loader class
        """
        for loader in self._loaders:
            if loader.name == meta.loader:
                return loader

        if raise_on_error:
            raise ImproperlyConfigured(
                "Resource has invalid loader '{}': {}\nAvailiable loaders: {}".format(
                    meta.loader, meta, [loader.name for loader in self._loaders]))