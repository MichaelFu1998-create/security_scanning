def addto_collection(self, collection, payload):
        """
        Add one or more items to a collection
        Accepts two arguments:
        The collection ID, and an item dict
        """
        ident = payload["key"]
        modified = payload["version"]
        # add the collection data from the item
        modified_collections = payload["data"]["collections"] + [collection]
        headers = {"If-Unmodified-Since-Version": str(modified)}
        headers.update(self.default_headers())
        req = requests.patch(
            url=self.endpoint
            + "/{t}/{u}/items/{i}".format(
                t=self.library_type, u=self.library_id, i=ident
            ),
            data=json.dumps({"collections": modified_collections}),
            headers=headers,
        )
        self.request = req
        try:
            req.raise_for_status()
        except requests.exceptions.HTTPError:
            error_handler(req)
        return True