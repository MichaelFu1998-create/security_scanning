def get_stores(self, names=None, workspaces=None):
        '''
          Returns a list of stores in the catalog. If workspaces is specified will only return stores in those workspaces.
          If names is specified, will only return stores that match.
          names can either be a comma delimited string or an array.
          Will return an empty list if no stores are found.
        '''

        if isinstance(workspaces, Workspace):
            workspaces = [workspaces]
        elif isinstance(workspaces, list) and [w for w in workspaces if isinstance(w, Workspace)]:
            # nothing
            pass
        else:
            workspaces = self.get_workspaces(names=workspaces)

        stores = []
        for ws in workspaces:
            ds_list = self.get_xml(ws.datastore_url)
            cs_list = self.get_xml(ws.coveragestore_url)
            wms_list = self.get_xml(ws.wmsstore_url)
            stores.extend([datastore_from_index(self, ws, n) for n in ds_list.findall("dataStore")])
            stores.extend([coveragestore_from_index(self, ws, n) for n in cs_list.findall("coverageStore")])
            stores.extend([wmsstore_from_index(self, ws, n) for n in wms_list.findall("wmsStore")])

        if names is None:
            names = []
        elif isinstance(names, basestring):
            names = [s.strip() for s in names.split(',') if s.strip()]

        if stores and names:
            return ([store for store in stores if store.name in names])

        return stores