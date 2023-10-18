def shared_blockchain_instance(self):
        """ This method will initialize ``SharedInstance.instance`` and return it.
            The purpose of this method is to have offer single default
            instance that can be reused by multiple classes.
        """
        if not self._sharedInstance.instance:
            klass = self.get_instance_class()
            self._sharedInstance.instance = klass(**self._sharedInstance.config)
        return self._sharedInstance.instance