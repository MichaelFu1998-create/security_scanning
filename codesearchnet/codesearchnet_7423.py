def create_collections(self, payload, last_modified=None):
        """
        Create new Zotero collections
        Accepts one argument, a list of dicts containing the following keys:

        'name': the name of the collection
        'parentCollection': OPTIONAL, the parent collection to which you wish to add this
        """
        # no point in proceeding if there's no 'name' key
        for item in payload:
            if "name" not in item:
                raise ze.ParamNotPassed("The dict you pass must include a 'name' key")
            # add a blank 'parentCollection' key if it hasn't been passed
            if "parentCollection" not in item:
                item["parentCollection"] = ""
        headers = {"Zotero-Write-Token": token()}
        if last_modified is not None:
            headers["If-Unmodified-Since-Version"] = str(last_modified)
        headers.update(self.default_headers())
        req = requests.post(
            url=self.endpoint
            + "/{t}/{u}/collections".format(t=self.library_type, u=self.library_id),
            headers=headers,
            data=json.dumps(payload),
        )
        self.request = req
        try:
            req.raise_for_status()
        except requests.exceptions.HTTPError:
            error_handler(req)
        return req.json()