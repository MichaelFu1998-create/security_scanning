def get_settings(self):
        """Returns the settings of the index."""
        try:
            logger.info('GET SETTINGS ON %s', self.index_name)
            return self.__index.get_settings()
        except AlgoliaException as e:
            if DEBUG:
                raise e
            else:
                logger.warning('ERROR DURING GET_SETTINGS ON %s: %s',
                               self.model, e)