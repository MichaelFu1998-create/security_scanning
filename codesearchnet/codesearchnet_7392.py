def num_collectionitems(self, collection):
        """ Return the total number of items in the specified collection
        """
        query = "/{t}/{u}/collections/{c}/items".format(
            u=self.library_id, t=self.library_type, c=collection.upper()
        )
        return self._totals(query)