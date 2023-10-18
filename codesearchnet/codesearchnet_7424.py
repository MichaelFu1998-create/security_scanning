def update_collection(self, payload, last_modified=None):
        """
        Update a Zotero collection property such as 'name'
        Accepts one argument, a dict containing collection data retrieved
        using e.g. 'collections()'
        """
        modified = payload["version"]
        if last_modified is not None:
            modified = last_modified
        key = payload["key"]
        headers = {"If-Unmodified-Since-Version": str(modified)}
        headers.update(self.default_headers())
        headers.update({"Content-Type": "application/json"})
        req = requests.put(
            url=self.endpoint
            + "/{t}/{u}/collections/{c}".format(
                t=self.library_type, u=self.library_id, c=key
            ),
            headers=headers,
            data=json.dumps(payload),
        )
        self.request = req
        try:
            req.raise_for_status()
        except requests.exceptions.HTTPError:
            error_handler(req)
        return True