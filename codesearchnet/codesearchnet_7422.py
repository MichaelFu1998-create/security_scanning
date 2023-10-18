def create_items(self, payload, parentid=None, last_modified=None):
        """
        Create new Zotero items
        Accepts two arguments:
            a list containing one or more item dicts
            an optional parent item ID.
        Note that this can also be used to update existing items
        """
        if len(payload) > 50:
            raise ze.TooManyItems("You may only create up to 50 items per call")
        # TODO: strip extra data if it's an existing item
        headers = {"Zotero-Write-Token": token(), "Content-Type": "application/json"}
        if last_modified is not None:
            headers["If-Unmodified-Since-Version"] = str(last_modified)
        to_send = json.dumps([i for i in self._cleanup(*payload, allow=("key"))])
        headers.update(self.default_headers())
        req = requests.post(
            url=self.endpoint
            + "/{t}/{u}/items".format(t=self.library_type, u=self.library_id),
            data=to_send,
            headers=dict(headers),
        )
        self.request = req
        try:
            req.raise_for_status()
        except requests.exceptions.HTTPError:
            error_handler(req)
        resp = req.json()
        if parentid:
            # we need to create child items using PATCH
            # TODO: handle possibility of item creation + failed parent
            # attachment
            uheaders = {
                "If-Unmodified-Since-Version": req.headers["last-modified-version"]
            }
            uheaders.update(self.default_headers())
            for value in resp["success"].values():
                payload = json.dumps({"parentItem": parentid})
                presp = requests.patch(
                    url=self.endpoint
                    + "/{t}/{u}/items/{v}".format(
                        t=self.library_type, u=self.library_id, v=value
                    ),
                    data=payload,
                    headers=dict(uheaders),
                )
                self.request = presp
                try:
                    presp.raise_for_status()
                except requests.exceptions.HTTPError:
                    error_handler(presp)
        return resp