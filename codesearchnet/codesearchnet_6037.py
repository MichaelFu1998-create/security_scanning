def get_style(self, name, workspace=None):
        '''
          returns a single style object.
          Will return None if no style is found.
          Will raise an error if more than one style with the same name is found.
        '''

        styles = self.get_styles(names=name, workspaces=workspace)
        return self._return_first_item(styles)