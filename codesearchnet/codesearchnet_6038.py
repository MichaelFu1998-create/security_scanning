def get_workspaces(self, names=None):
        '''
          Returns a list of workspaces in the catalog.
          If names is specified, will only return workspaces that match.
          names can either be a comma delimited string or an array.
          Will return an empty list if no workspaces are found.
        '''
        if names is None:
            names = []
        elif isinstance(names, basestring):
            names = [s.strip() for s in names.split(',') if s.strip()]

        data = self.get_xml("{}/workspaces.xml".format(self.service_url))
        workspaces = []
        workspaces.extend([workspace_from_index(self, node) for node in data.findall("workspace")])

        if workspaces and names:
            return ([ws for ws in workspaces if ws.name in names])

        return workspaces