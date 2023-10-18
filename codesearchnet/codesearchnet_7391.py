def publications(self):
        """ Return the contents of My Publications
        """
        if self.library_type != "users":
            raise ze.CallDoesNotExist(
                "This API call does not exist for group libraries"
            )
        query_string = "/{t}/{u}/publications/items"
        return self._build_query(query_string)