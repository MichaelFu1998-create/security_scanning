def add_granule(self, data, store, workspace=None):
        '''Harvest/add a granule into an existing imagemosaic'''
        ext = os.path.splitext(data)[-1]
        if ext == ".zip":
            type = "file.imagemosaic"
            upload_data = open(data, 'rb')
            headers = {
                "Content-type": "application/zip",
                "Accept": "application/xml"
            }
        else:
            type = "external.imagemosaic"
            upload_data = data if data.startswith("file:") else "file:{data}".format(data=data)
            headers = {
                "Content-type": "text/plain",
                "Accept": "application/xml"
            }

        params = dict()
        workspace_name = workspace
        if isinstance(store, basestring):
            store_name = store
        else:
            store_name = store.name
            workspace_name = store.workspace.name

        if workspace_name is None:
            raise ValueError("Must specify workspace")

        url = build_url(
            self.service_url,
            [
                "workspaces",
                workspace_name,
                "coveragestores",
                store_name,
                type
            ],
            params
        )

        try:
            resp = self.http_request(url, method='post', data=upload_data, headers=headers)
            if resp.status_code != 202:
                FailedRequestError('Failed to add granule to mosaic {} : {}, {}'.format(store, resp.status_code, resp.text))
            self._cache.clear()
        finally:
            if hasattr(upload_data, "close"):
                upload_data.close()

        # maybe return a list of all granules?
        return None