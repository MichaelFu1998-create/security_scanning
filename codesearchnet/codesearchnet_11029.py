def add(self, meta):
        """
        Add a resource to this pool.
        The resource is loaded and returned when ``load_pool()`` is called.

        :param meta: The resource description
        """
        self._check_meta(meta)
        self.resolve_loader(meta)
        self._resources.append(meta)