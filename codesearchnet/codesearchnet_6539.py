def delete_record(self, instance):
        """Deletes the record."""
        objectID = self.objectID(instance)
        try:
            self.__index.delete_object(objectID)
            logger.info('DELETE %s FROM %s', objectID, self.model)
        except AlgoliaException as e:
            if DEBUG:
                raise e
            else:
                logger.warning('%s FROM %s NOT DELETED: %s', objectID,
                               self.model, e)