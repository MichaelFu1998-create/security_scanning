def save(self, *args, **kwargs):
        """Overridden method that handles that re-ranking of objects and the
        integrity of the ``rank`` field.

        :param rerank:
            Added parameter, if True will rerank other objects based on the
            change in this save.  Defaults to True.  
        """
        rerank = kwargs.pop('rerank', True)
        if rerank:
            if not self.id:
                self._process_new_rank_obj()
            elif self.rank == self._rank_at_load:
                # nothing changed
                pass
            else:
                self._process_moved_rank_obj()

        super(RankedModel, self).save(*args, **kwargs)