def _make_namespace(self) -> Namespace:
        """Make a namespace."""
        namespace = Namespace(
            name=self._get_namespace_name(),
            keyword=self._get_namespace_keyword(),
            url=self._get_namespace_url(),
            version=str(time.asctime()),
        )
        self.session.add(namespace)

        entries = self._get_namespace_entries(namespace)
        self.session.add_all(entries)

        t = time.time()
        log.info('committing models')
        self.session.commit()
        log.info('committed models in %.2f seconds', time.time() - t)

        return namespace