def __post_save_receiver(self, instance, **kwargs):
        """Signal handler for when a registered model has been saved."""
        logger.debug('RECEIVE post_save FOR %s', instance.__class__)
        self.save_record(instance, **kwargs)