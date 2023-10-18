def mosaic_coverages(self, store):
        '''Returns all coverages in a coverage store'''
        params = dict()
        url = build_url(
            self.service_url,
            [
                "workspaces",
                store.workspace.name,
                "coveragestores",
                store.name,
                "coverages.json"
            ],
            params
        )
        # GET /workspaces/<ws>/coveragestores/<name>/coverages.json
        headers = {
            "Content-type": "application/json",
            "Accept": "application/json"
        }

        resp = self.http_request(url, headers=headers)
        if resp.status_code != 200:
            FailedRequestError('Failed to get mosaic coverages {} : {}, {}'.format(store, resp.status_code, resp.text))

        self._cache.clear()
        return resp.json()