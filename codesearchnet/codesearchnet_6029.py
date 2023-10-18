def list_granules(self, coverage, store, workspace=None, filter=None, limit=None, offset=None):
        '''List granules of an imagemosaic'''
        params = dict()

        if filter is not None:
            params['filter'] = filter
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset

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
                "coverages",
                coverage,
                "index/granules.json"
            ],
            params
        )

        # GET /workspaces/<ws>/coveragestores/<name>/coverages/<coverage>/index/granules.json
        headers = {
            "Content-type": "application/json",
            "Accept": "application/json"
        }

        resp = self.http_request(url, headers=headers)
        if resp.status_code != 200:
            FailedRequestError('Failed to list granules in mosaic {} : {}, {}'.format(store, resp.status_code, resp.text))

        self._cache.clear()
        return resp.json()