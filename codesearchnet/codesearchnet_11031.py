def resolve_loader(self, meta: ResourceDescription):
        """
        Attempts to assign a loader class to a resource description

        :param meta: The resource description instance
        """
        meta.loader_cls = self.get_loader(meta, raise_on_error=True)