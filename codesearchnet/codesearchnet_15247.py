def _update_namespace(self, namespace: Namespace) -> None:
        """Update an already-created namespace.

        Note: Only call this if namespace won't be none!
        """
        old_entry_identifiers = self._get_old_entry_identifiers(namespace)
        new_count = 0
        skip_count = 0

        for model in self._iterate_namespace_models():
            if self._get_identifier(model) in old_entry_identifiers:
                continue

            entry = self._create_namespace_entry_from_model(model, namespace=namespace)
            if entry is None or entry.name is None:
                skip_count += 1
                continue

            new_count += 1
            self.session.add(entry)

        t = time.time()
        log.info('got %d new entries. skipped %d entries missing names. committing models', new_count, skip_count)
        self.session.commit()
        log.info('committed models in %.2f seconds', time.time() - t)