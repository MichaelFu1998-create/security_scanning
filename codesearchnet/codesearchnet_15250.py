def upload_bel_namespace(self, update: bool = False) -> Namespace:
        """Upload the namespace to the PyBEL database.

        :param update: Should the namespace be updated first?
        """
        if not self.is_populated():
            self.populate()

        namespace = self._get_default_namespace()

        if namespace is None:
            log.info('making namespace for %s', self._get_namespace_name())
            return self._make_namespace()

        if update:
            self._update_namespace(namespace)

        return namespace