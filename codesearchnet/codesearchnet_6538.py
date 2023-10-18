def save_record(self, instance, update_fields=None, **kwargs):
        """Saves the record.

        If `update_fields` is set, this method will use partial_update_object()
        and will update only the given fields (never `_geoloc` and `_tags`).

        For more information about partial_update_object:
        https://github.com/algolia/algoliasearch-client-python#update-an-existing-object-in-the-index
        """
        if not self._should_index(instance):
            # Should not index, but since we don't now the state of the
            # instance, we need to send a DELETE request to ensure that if
            # the instance was previously indexed, it will be removed.
            self.delete_record(instance)
            return

        try:
            if update_fields:
                obj = self.get_raw_record(instance,
                                          update_fields=update_fields)
                result = self.__index.partial_update_object(obj)
            else:
                obj = self.get_raw_record(instance)
                result = self.__index.save_object(obj)
            logger.info('SAVE %s FROM %s', obj['objectID'], self.model)
            return result
        except AlgoliaException as e:
            if DEBUG:
                raise e
            else:
                logger.warning('%s FROM %s NOT SAVED: %s', obj['objectID'],
                               self.model, e)