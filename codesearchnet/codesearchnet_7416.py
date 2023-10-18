def delete_saved_search(self, keys):
        """ Delete one or more saved searches by passing a list of one or more
        unique search keys
        """
        headers = {"Zotero-Write-Token": token()}
        headers.update(self.default_headers())
        req = requests.delete(
            url=self.endpoint
            + "/{t}/{u}/searches".format(t=self.library_type, u=self.library_id),
            headers=headers,
            params={"searchKey": ",".join(keys)},
        )
        self.request = req
        try:
            req.raise_for_status()
        except requests.exceptions.HTTPError:
            error_handler(req)
        return req.status_code