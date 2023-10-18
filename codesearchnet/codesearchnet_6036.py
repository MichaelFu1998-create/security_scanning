def get_styles(self, names=None, workspaces=None):
        '''
        names and workspaces can be provided as a comma delimited strings or as arrays, and are used for filtering.
        If no workspaces are provided, will return all styles in the catalog (global and workspace specific).
        Will always return an array.
        '''

        all_styles = []

        if workspaces is None:
            # Add global styles
            url = "{}/styles.xml".format(self.service_url)
            styles = self.get_xml(url)
            all_styles.extend([Style(self, s.find('name').text) for s in styles.findall("style")])
            workspaces = []
        elif isinstance(workspaces, basestring):
            workspaces = [s.strip() for s in workspaces.split(',') if s.strip()]
        elif isinstance(workspaces, Workspace):
            workspaces = [workspaces]

        if not workspaces:
            workspaces = self.get_workspaces()

        for ws in workspaces:
            url = "{}/workspaces/{}/styles.xml".format(self.service_url, _name(ws))
            try:
                styles = self.get_xml(url)
            except FailedRequestError as e:
                if "no such workspace" in str(e).lower():
                    continue
                elif "workspace {} not found".format(_name(ws)) in str(e).lower():
                    continue
                else:
                    raise FailedRequestError("Failed to get styles: {}".format(e))

            all_styles.extend([Style(self, s.find("name").text, _name(ws)) for s in styles.findall("style")])

        if names is None:
            names = []
        elif isinstance(names, basestring):
            names = [s.strip() for s in names.split(',') if s.strip()]

        if all_styles and names:
            return ([style for style in all_styles if style.name in names])

        return all_styles