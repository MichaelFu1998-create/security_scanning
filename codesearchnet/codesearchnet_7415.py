def saved_search(self, name, conditions):
        """ Create a saved search. conditions is a list of dicts
        containing search conditions, and must contain the following str keys:
        condition, operator, value
        """
        self.savedsearch._validate(conditions)
        payload = [{"name": name, "conditions": conditions}]
        headers = {"Zotero-Write-Token": token()}
        headers.update(self.default_headers())
        req = requests.post(
            url=self.endpoint
            + "/{t}/{u}/searches".format(t=self.library_type, u=self.library_id),
            headers=headers,
            data=json.dumps(payload),
        )
        self.request = req
        try:
            req.raise_for_status()
        except requests.exceptions.HTTPError:
            error_handler(req)
        return req.json()