def file(self, item, **kwargs):
        """ Get the file from an specific item
        """
        query_string = "/{t}/{u}/items/{i}/file".format(
            u=self.library_id, t=self.library_type, i=item.upper()
        )
        return self._build_query(query_string, no_params=True)