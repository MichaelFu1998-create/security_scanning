def load(self, meta: ResourceDescription) -> Any:
        """
        Loads a resource or return existing one

        :param meta: The resource description
        """
        self._check_meta(meta)
        self.resolve_loader(meta)
        return meta.loader_cls(meta).load()