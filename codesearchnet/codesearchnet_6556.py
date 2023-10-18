def __pre_delete_receiver(self, instance, **kwargs):
        """Signal handler for when a registered model has been deleted."""
        logger.debug('RECEIVE pre_delete FOR %s', instance.__class__)
        self.delete_record(instance)