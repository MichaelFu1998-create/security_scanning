def get_workspace(self, name):
        '''
          returns a single workspace object.
          Will return None if no workspace is found.
          Will raise an error if more than one workspace with the same name is found.
        '''

        workspaces = self.get_workspaces(names=name)
        return self._return_first_item(workspaces)