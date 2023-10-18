def fulltext_item(self, itemkey, **kwargs):
        """ Get full-text content for an item"""
        query_string = "/{t}/{u}/items/{itemkey}/fulltext".format(
            t=self.library_type, u=self.library_id, itemkey=itemkey
        )
        return self._build_query(query_string)