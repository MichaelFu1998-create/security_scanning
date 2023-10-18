def drop_bel_namespace(self) -> Optional[Namespace]:
        """Remove the default namespace if it exists."""
        namespace = self._get_default_namespace()

        if namespace is not None:
            for entry in tqdm(namespace.entries, desc=f'deleting entries in {self._get_namespace_name()}'):
                self.session.delete(entry)
            self.session.delete(namespace)

            log.info('committing deletions')
            self.session.commit()
            return namespace