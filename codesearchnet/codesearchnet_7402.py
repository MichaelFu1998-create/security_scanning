def all_collections(self, collid=None):
        """
        Retrieve all collections and subcollections. Works for top-level collections
        or for a specific collection. Works at all collection depths.
        """
        all_collections = []

        def subcoll(clct):
            """ recursively add collections to a flat master list """
            all_collections.append(clct)
            if clct["meta"].get("numCollections", 0) > 0:
                # add collection to master list & recur with all child
                # collections
                [
                    subcoll(c)
                    for c in self.everything(self.collections_sub(clct["data"]["key"]))
                ]

        # select all top-level collections or a specific collection and
        # children
        if collid:
            toplevel = [self.collection(collid)]
        else:
            toplevel = self.everything(self.collections_top())
        [subcoll(collection) for collection in toplevel]
        return all_collections