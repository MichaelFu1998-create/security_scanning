def validate_sceneInfo(self):
        """Check whether sceneInfo is valid to download from AWS Storage."""
        if self.sceneInfo.prefix not in self.__prefixesValid:
            raise WrongSceneNameError('AWS: Prefix of %s (%s) is invalid'
                % (self.sceneInfo.name, self.sceneInfo.prefix))