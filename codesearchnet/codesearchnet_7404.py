def tags(self, **kwargs):
        """ Get tags
        """
        query_string = "/{t}/{u}/tags"
        self.tag_data = True
        return self._build_query(query_string)