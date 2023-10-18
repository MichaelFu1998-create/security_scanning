def check_items(self, items):
        """
        Check that items to be created contain no invalid dict keys
        Accepts a single argument: a list of one or more dicts
        The retrieved fields are cached and re-used until a 304 call fails
        """
        # check for a valid cached version
        if self.templates.get("item_fields") and not self._updated(
            "/itemFields", self.templates["item_fields"], "item_fields"
        ):
            template = set(t["field"] for t in self.templates["item_fields"]["tmplt"])
        else:
            template = set(t["field"] for t in self.item_fields())
        # add fields we know to be OK
        template = template | set(
            [
                "path",
                "tags",
                "notes",
                "itemType",
                "creators",
                "mimeType",
                "linkMode",
                "note",
                "charset",
                "dateAdded",
                "version",
                "collections",
                "dateModified",
                "relations",
                #  attachment items
                "parentItem",
                "mtime",
                "contentType",
                "md5",
                "filename",
            ]
        )
        template = template | set(self.temp_keys)
        for pos, item in enumerate(items):
            if set(item) == set(["links", "library", "version", "meta", "key", "data"]):
                # we have an item that was retrieved from the API
                item = item["data"]
            to_check = set(i for i in list(item.keys()))
            difference = to_check.difference(template)
            if difference:
                raise ze.InvalidItemFields(
                    "Invalid keys present in item %s: %s"
                    % (pos + 1, " ".join(i for i in difference))
                )
        return items