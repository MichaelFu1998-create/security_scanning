def get_resource(self, name=None, store=None, workspace=None):
        '''
          returns a single resource object.
          Will return None if no resource is found.
          Will raise an error if more than one resource with the same name is found.
        '''

        resources = self.get_resources(names=name, stores=store, workspaces=workspace)
        return self._return_first_item(resources)