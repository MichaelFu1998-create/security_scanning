def reindex_all(self, model, batch_size=1000):
        """
        Reindex all the records.

        By default, this method use Model.objects.all() but you can implement
        a method `get_queryset` in your subclass. This can be used to optimize
        the performance (for example with select_related or prefetch_related).
        """
        adapter = self.get_adapter(model)
        return adapter.reindex_all(batch_size)