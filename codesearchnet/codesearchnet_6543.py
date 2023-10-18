def set_settings(self):
        """Applies the settings to the index."""
        if not self.settings:
            return

        try:
            self.__index.set_settings(self.settings)
            logger.info('APPLY SETTINGS ON %s', self.index_name)
        except AlgoliaException as e:
            if DEBUG:
                raise e
            else:
                logger.warning('SETTINGS NOT APPLIED ON %s: %s',
                               self.model, e)