def get_layergroup(self, name, workspace=None):
        '''
          returns a single layergroup object.
          Will return None if no layergroup is found.
          Will raise an error if more than one layergroup with the same name is found.
        '''

        layergroups = self.get_layergroups(names=name, workspaces=workspace)
        return self._return_first_item(layergroups)