def get_layergroups(self, names=None, workspaces=None):
        '''
        names and workspaces can be provided as a comma delimited strings or as arrays, and are used for filtering.
        If no workspaces are provided, will return all layer groups in the catalog (global and workspace specific).
        Will always return an array.
        '''

        layergroups = []

        if workspaces is None or len(workspaces) == 0:
            # Add global layergroups
            url = "{}/layergroups.xml".format(self.service_url)
            groups = self.get_xml(url)
            layergroups.extend([LayerGroup(self, g.find("name").text, None) for g in groups.findall("layerGroup")])
            workspaces = []
        elif isinstance(workspaces, basestring):
            workspaces = [s.strip() for s in workspaces.split(',') if s.strip()]
        elif isinstance(workspaces, Workspace):
            workspaces = [workspaces]

        if not workspaces:
            workspaces = self.get_workspaces()

        for ws in workspaces:
            ws_name = _name(ws)
            url = "{}/workspaces/{}/layergroups.xml".format(self.service_url, ws_name)
            try:
                groups = self.get_xml(url)
            except FailedRequestError as e:
                if "no such workspace" in str(e).lower():
                    continue
                else:
                    raise FailedRequestError("Failed to get layergroups: {}".format(e))

            layergroups.extend([LayerGroup(self, g.find("name").text, ws_name) for g in groups.findall("layerGroup")])

        if names is None:
            names = []
        elif isinstance(names, basestring):
            names = [s.strip() for s in names.split(',') if s.strip()]

        if layergroups and names:
            return ([lg for lg in layergroups if lg.name in names])

        return layergroups