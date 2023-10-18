def delete_item(self, payload, last_modified=None):
        """
        Delete Items from a Zotero library
        Accepts a single argument:
            a dict containing item data
            OR a list of dicts containing item data
        """
        params = None
        if isinstance(payload, list):
            params = {"itemKey": ",".join([p["key"] for p in payload])}
            if last_modified is not None:
                modified = last_modified
            else:
                modified = payload[0]["version"]
            url = self.endpoint + "/{t}/{u}/items".format(
                t=self.library_type, u=self.library_id
            )
        else:
            ident = payload["key"]
            if last_modified is not None:
                modified = last_modified
            else:
                modified = payload["version"]
            url = self.endpoint + "/{t}/{u}/items/{c}".format(
                t=self.library_type, u=self.library_id, c=ident
            )
        headers = {"If-Unmodified-Since-Version": str(modified)}
        headers.update(self.default_headers())
        req = requests.delete(url=url, params=params, headers=headers)
        self.request = req
        try:
            req.raise_for_status()
        except requests.exceptions.HTTPError:
            error_handler(req)
        return True