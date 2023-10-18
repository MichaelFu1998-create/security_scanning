def collections_sub(self, collection, **kwargs):
        """ Get subcollections for a specific collection
        """
        query_string = "/{t}/{u}/collections/{c}/collections".format(
            u=self.library_id, t=self.library_type, c=collection.upper()
        )
        return self._build_query(query_string)