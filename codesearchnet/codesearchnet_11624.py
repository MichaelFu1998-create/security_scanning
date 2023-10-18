def unpublish(self, registry=None):
        ''' Try to un-publish the current version. Return a description of any
            errors that occured, or None if successful.
        '''
        return registry_access.unpublish(
            self.getRegistryNamespace(),
            self.getName(),
            self.getVersion(),
            registry=registry
        )