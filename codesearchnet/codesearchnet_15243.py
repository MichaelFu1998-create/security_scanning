def _iterate_namespace_models(self, **kwargs) -> Iterable:
        """Return an iterator over the models to be converted to the namespace."""
        return tqdm(
            self._get_query(self.namespace_model),
            total=self._count_model(self.namespace_model),
            **kwargs
        )