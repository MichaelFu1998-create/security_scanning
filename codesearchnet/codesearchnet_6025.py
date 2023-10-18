def get_store(self, name, workspace=None):
        '''
          Returns a single store object.
          Will return None if no store is found.
          Will raise an error if more than one store with the same name is found.
        '''

        stores = self.get_stores(workspaces=workspace, names=name)
        return self._return_first_item(stores)