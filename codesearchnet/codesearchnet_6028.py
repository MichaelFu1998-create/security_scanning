def delete_granule(self, coverage, store, granule_id, workspace=None):
        '''Deletes a granule of an existing imagemosaic'''
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
                "coverages",
                coverage,
                "index/granules",
                granule_id,
                ".json"
            ],
            params
        )

        # DELETE /workspaces/<ws>/coveragestores/<name>/coverages/<coverage>/index/granules/<granule_id>.json
        headers = {
            "Content-type": "application/json",
            "Accept": "application/json"
        }

        resp = self.http_request(url, method='delete', headers=headers)
        if resp.status_code != 200:
            FailedRequestError('Failed to delete granule from mosaic {} : {}, {}'.format(store, resp.status_code, resp.text))
        self._cache.clear()

        # maybe return a list of all granules?
        return None