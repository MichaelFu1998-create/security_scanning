def validate_sceneInfo(self):
        """Check scene name and whether remote file exists. Raises
        WrongSceneNameError if the scene name is wrong.
        """
        if self.sceneInfo.prefix not in self.__satellitesMap:
            logger.error('Google Downloader: Prefix of %s (%s) is invalid'
                % (self.sceneInfo.name, self.sceneInfo.prefix))
            raise WrongSceneNameError('Google Downloader: Prefix of %s (%s) is invalid'
                % (self.sceneInfo.name, self.sceneInfo.prefix))