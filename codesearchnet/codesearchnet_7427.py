def update_item(self, payload, last_modified=None):
        """
        Update an existing item
        Accepts one argument, a dict containing Item data
        """
        to_send = self.check_items([payload])[0]
        if last_modified is None:
            modified = payload["version"]
        else:
            modified = last_modified
        ident = payload["key"]
        headers = {"If-Unmodified-Since-Version": str(modified)}
        headers.update(self.default_headers())
        req = requests.patch(
            url=self.endpoint
            + "/{t}/{u}/items/{id}".format(
                t=self.library_type, u=self.library_id, id=ident
            ),
            headers=headers,
            data=json.dumps(to_send),
        )
        self.request = req
        try:
            req.raise_for_status()
        except requests.exceptions.HTTPError:
            error_handler(req)
        return True