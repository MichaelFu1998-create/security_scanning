def get_resources(self, names=None, stores=None, workspaces=None):
        '''
        Resources include feature stores, coverage stores and WMS stores, however does not include layer groups.
        names, stores and workspaces can be provided as a comma delimited strings or as arrays, and are used for filtering.
        Will always return an array.
        '''

        stores = self.get_stores(
            names = stores,
            workspaces = workspaces
        )

        resources = []
        for s in stores:
            try:
                resources.extend(s.get_resources())
            except FailedRequestError:
                continue

        if names is None:
            names = []
        elif isinstance(names, basestring):
            names = [s.strip() for s in names.split(',') if s.strip()]

        if resources and names:
            return ([resource for resource in resources if resource.name in names])

        return resources